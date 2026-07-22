// OpenMontage Desktop - Tauri shell for OpenMontage AI video production system
// Manages Python Backlot server as sidecar, loads Backlot UI in webview

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use tauri::State;

struct AppState {
    backlot_process: Mutex<Option<Child>>,
    config: Mutex<HashMap<String, String>>,
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

fn find_python() -> Option<String> {
    let candidates = if cfg!(target_os = "windows") {
        vec!["python", "python3", "py"]
    } else {
        vec!["python3", "python"]
    };
    for cmd in candidates {
        if let Ok(output) = Command::new(cmd).arg("--version").output() {
            if output.status.success() {
                return Some(cmd.to_string());
            }
        }
    }
    None
}

fn project_root() -> std::path::PathBuf {
    // In dev: parent of desktop-shell/
    // In prod: resource dir
    let exe_dir = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_default();

    // Check if we're in a bundle (Resources dir)
    if let Some(resources) = exe_dir.parent().and_then(|p| p.parent()) {
        let bundled = resources.join("openmontage");
        if bundled.exists() {
            return bundled;
        }
    }

    // Dev mode: walk up from desktop-shell
    let dev_root = std::env::current_dir()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_default();
    dev_root
}

#[tauri::command]
fn start_backlot(state: State<AppState>, port: Option<u16>) -> Result<BacklotStatus, String> {
    let port = port.unwrap_or(4750);
    let mut proc_guard = state.backlot_process.lock().map_err(|e| e.to_string())?;

    // Check if already running
    if let Some(ref mut child) = *proc_guard {
        if child.try_wait().ok().flatten().is_none() {
            return Ok(BacklotStatus {
                running: true,
                port,
                url: format!("http://127.0.0.1:{}", port),
            });
        }
    }

    let python = find_python().ok_or("Python not found. Please install Python 3.10+")?;
    let root = project_root();

    let child = Command::new(&python)
        .args(["-m", "backlot", "serve", "--port", &port.to_string()])
        .current_dir(&root)
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .stdin(Stdio::null())
        .spawn()
        .map_err(|e| format!("Failed to start Backlot: {}", e))?;

    *proc_guard = Some(child);

    // Wait for server to be ready
    let url = format!("http://127.0.0.1:{}", port);
    for _ in 0..30 {
        std::thread::sleep(std::time::Duration::from_millis(500));
        if ureq::get(&format!("{}/api/health", url)).call().is_ok() {
            return Ok(BacklotStatus {
                running: true,
                port,
                url,
            });
        }
    }

    Ok(BacklotStatus {
        running: true,
        port,
        url,
    })
}

#[tauri::command]
fn stop_backlot(state: State<AppState>) -> Result<(), String> {
    let mut proc_guard = state.backlot_process.lock().map_err(|e| e.to_string())?;
    if let Some(ref mut child) = *proc_guard {
        child.kill().map_err(|e| e.to_string())?;
        *proc_guard = None;
    }
    Ok(())
}

#[tauri::command]
fn get_backlot_status(state: State<AppState>) -> Result<BacklotStatus, String> {
    let proc_guard = state.backlot_process.lock().map_err(|e| e.to_string())?;
    let running = proc_guard
        .as_ref()
        .map(|_| true)
        .unwrap_or(false);
    Ok(BacklotStatus {
        running,
        port: 4750,
        url: "http://127.0.0.1:4750".to_string(),
    })
}

#[tauri::command]
fn save_api_key(state: State<AppState>, entry: ApiKeyEntry) -> Result<(), String> {
    let mut config = state.config.lock().map_err(|e| e.to_string())?;
    config.insert(entry.key.clone(), entry.value.clone());

    // Also write to .env file
    let root = project_root();
    let env_path = root.join(".env");
    let mut env_content = std::fs::read_to_string(&env_path).unwrap_or_default();

    let key_line = format!("{}={}", entry.key, entry.value);
    if env_content.contains(&format!("{}=", entry.key)) {
        // Replace existing
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
        env_content.push_str(&format!("\n{}", key_line));
    }

    std::fs::write(&env_path, env_content).map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn get_api_key(state: State<AppState>, key: String) -> Result<String, String> {
    let config = state.config.lock().map_err(|e| e.to_string())?;
    Ok(config.get(&key).cloned().unwrap_or_default())
}

#[tauri::command]
fn load_env_keys(state: State<AppState>) -> Result<HashMap<String, String>, String> {
    let root = project_root();
    let env_path = root.join(".env");
    let mut result = HashMap::new();

    if let Ok(content) = std::fs::read_to_string(&env_path) {
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

    let mut config = state.config.lock().map_err(|e| e.to_string())?;
    *config = result.clone();
    Ok(result)
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(AppState {
            backlot_process: Mutex::new(None),
            config: Mutex::new(HashMap::new()),
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
