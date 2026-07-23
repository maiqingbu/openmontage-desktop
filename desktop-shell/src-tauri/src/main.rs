// OpenMontage Desktop - Tauri shell for OpenMontage AI video production system
// 生产模式：拉起打包好的 backlot-server sidecar（PyInstaller 独立二进制）
// 开发模式：回退到系统 python -m backlot serve
// 用户数据（.env / projects）存放在应用数据目录，保证安装后可写。

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use tauri::{AppHandle, Manager, State};
use tauri_plugin_shell::process::{CommandChild, CommandEvent};
use tauri_plugin_shell::ShellExt;

enum ChildKind {
    Sidecar(CommandChild),
    Python(Child),
}

struct AppState {
    backlot_process: Mutex<Option<ChildKind>>,
}

#[derive(Serialize, Deserialize)]
struct BacklotStatus {
    running: bool,
    port: u16,
    url: String,
}

#[derive(Serialize, Deserialize)]
struct ApiKeyEntry {
    key: String,
    value: String,
}

fn app_data_dir(app: &AppHandle) -> PathBuf {
    let dir = app
        .path()
        .app_data_dir()
        .unwrap_or_else(|_| std::env::temp_dir().join("openmontage-desktop"));
    let _ = std::fs::create_dir_all(&dir);
    dir
}

fn env_file_path(app: &AppHandle) -> PathBuf {
    app_data_dir(app).join(".env")
}

fn projects_dir(app: &AppHandle) -> PathBuf {
    let dir = app_data_dir(app).join("projects");
    let _ = std::fs::create_dir_all(&dir);
    dir
}

fn read_env_file(app: &AppHandle) -> HashMap<String, String> {
    let mut result = HashMap::new();
    if let Ok(content) = std::fs::read_to_string(env_file_path(app)) {
        for line in content.lines() {
            let line = line.trim();
            if line.is_empty() || line.starts_with('#') {
                continue;
            }
            if let Some(pos) = line.find('=') {
                let key = line[..pos].trim().to_string();
                let value = line[pos + 1..]
                    .split('#')
                    .next()
                    .unwrap_or("")
                    .trim()
                    .to_string();
                if !value.is_empty() {
                    result.insert(key, value);
                }
            }
        }
    }
    result
}

fn health_ok(port: u16) -> bool {
    ureq::get(&format!("http://127.0.0.1:{}/api/health", port))
        .timeout(std::time::Duration::from_millis(800))
        .call()
        .is_ok()
}

fn dev_project_root() -> PathBuf {
    // 开发模式：desktop-shell/src-tauri -> 仓库根
    std::env::current_dir()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_default()
}

#[tauri::command]
fn start_backlot(
    app: AppHandle,
    state: State<AppState>,
    port: Option<u16>,
) -> Result<BacklotStatus, String> {
    let port = port.unwrap_or(4750);
    let url = format!("http://127.0.0.1:{}", port);

    // 已在运行（包括外部已启动的情况）直接返回
    if health_ok(port) {
        return Ok(BacklotStatus {
            running: true,
            port,
            url,
        });
    }

    let mut proc_guard = state.backlot_process.lock().map_err(|e| e.to_string())?;
    if let Some(ChildKind::Python(child)) = proc_guard.as_mut() {
        if child.try_wait().ok().flatten().is_none() && health_ok(port) {
            return Ok(BacklotStatus {
                running: true,
                port,
                url,
            });
        }
    }

    // 注入 .env 中的全部 API Key，并指定 projects 目录
    let mut envs: Vec<(String, String)> = read_env_file(&app).into_iter().collect();
    envs.push((
        "OPENMONTAGE_PROJECTS_DIR".to_string(),
        projects_dir(&app).to_string_lossy().to_string(),
    ));

    // 优先 sidecar（生产包内置）；失败则回退系统 Python（开发模式）
    let mut spawned: Option<ChildKind> = None;
    match app.shell().sidecar("backlot-server") {
        Ok(cmd) => {
            let cmd = cmd.args(["--port", &port.to_string()]).envs(envs.clone());
            match cmd.spawn() {
                Ok((mut rx, child)) => {
                    tauri::async_runtime::spawn(async move {
                        while let Some(_event) = rx.recv().await {
                            if matches!(_event, CommandEvent::Terminated(_)) {
                                break;
                            }
                        }
                    });
                    spawned = Some(ChildKind::Sidecar(child));
                }
                Err(e) => eprintln!("sidecar 启动失败，回退 Python: {}", e),
            }
        }
        Err(e) => eprintln!("sidecar 不可用，回退 Python: {}", e),
    }

    if spawned.is_none() {
        let root = dev_project_root();
        let python = ["python3", "python"]
            .iter()
            .find(|cmd| {
                Command::new(cmd)
                    .arg("--version")
                    .output()
                    .map(|o| o.status.success())
                    .unwrap_or(false)
            })
            .ok_or("未找到 Python 3.10+，且内置服务不可用")?;
        let mut command = Command::new(python);
        command
            .args(["-m", "backlot", "serve", "--port", &port.to_string()])
            .current_dir(&root)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .stdin(Stdio::null());
        for (k, v) in &envs {
            command.env(k, v);
        }
        let child = command
            .spawn()
            .map_err(|e| format!("Backlot 启动失败: {}", e))?;
        spawned = Some(ChildKind::Python(child));
    }

    *proc_guard = spawned;

    // 等待服务就绪（最长 20 秒）
    for _ in 0..40 {
        std::thread::sleep(std::time::Duration::from_millis(500));
        if health_ok(port) {
            return Ok(BacklotStatus {
                running: true,
                port,
                url,
            });
        }
    }

    Err("服务启动超时，请查看日志".to_string())
}

#[tauri::command]
fn stop_backlot(state: State<AppState>) -> Result<(), String> {
    let mut proc_guard = state.backlot_process.lock().map_err(|e| e.to_string())?;
    if let Some(kind) = proc_guard.take() {
        match kind {
            ChildKind::Sidecar(child) => child.kill().map_err(|e| e.to_string())?,
            ChildKind::Python(mut child) => child.kill().map_err(|e| e.to_string())?,
        }
    }
    Ok(())
}

#[tauri::command]
fn get_backlot_status(state: State<AppState>) -> Result<BacklotStatus, String> {
    let port = 4750u16;
    let running = {
        let guard = state.backlot_process.lock().map_err(|e| e.to_string())?;
        guard.is_some()
    } || health_ok(port);
    Ok(BacklotStatus {
        running,
        port,
        url: format!("http://127.0.0.1:{}", port),
    })
}

#[tauri::command]
fn save_api_key(app: AppHandle, entry: ApiKeyEntry) -> Result<(), String> {
    let env_path = env_file_path(&app);
    let mut env_content = std::fs::read_to_string(&env_path).unwrap_or_default();

    let key_line = format!("{}={}", entry.key, entry.value);
    if env_content.contains(&format!("{}=", entry.key)) {
        let lines: Vec<String> = env_content
            .lines()
            .map(|l| {
                if l.starts_with(&format!("{}=", entry.key)) {
                    key_line.clone()
                } else {
                    l.to_string()
                }
            })
            .collect();
        env_content = lines.join("\n");
    } else {
        if !env_content.is_empty() && !env_content.ends_with('\n') {
            env_content.push('\n');
        }
        env_content.push_str(&key_line);
    }

    std::fs::write(&env_path, env_content).map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn get_api_key(app: AppHandle, key: String) -> Result<String, String> {
    Ok(read_env_file(&app).get(&key).cloned().unwrap_or_default())
}

#[tauri::command]
fn load_env_keys(app: AppHandle) -> Result<HashMap<String, String>, String> {
    Ok(read_env_file(&app))
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(AppState {
            backlot_process: Mutex::new(None),
        })
        .invoke_handler(tauri::generate_handler![
            start_backlot,
            stop_backlot,
            get_backlot_status,
            save_api_key,
            get_api_key,
            load_env_keys,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
