mod key_manager;
use key_manager::KeyManager;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::fs;
use tauri::Manager;

// Global key manager instance
static mut KEY_MANAGER: Option<Mutex<KeyManager>> = None;

#[derive(Serialize, Deserialize)]
struct PingRequest {
    token: String,
    message: String,
}

#[derive(Serialize, Deserialize)]
struct PingResponse {
    message: String,
}

#[derive(Serialize, Deserialize)]
struct GenerateSeedResponse {
    seed_phrase: String,
}

#[derive(Serialize, Deserialize)]
struct ImportSeedRequest {
    seed_phrase: String,
}

#[derive(Serialize, Deserialize)]
struct DeriveKeyRequest {
    seed_phrase: String,
    path: String,
}

#[derive(Serialize, Deserialize)]
struct DeriveKeyResponse {
    private_key: String,
}

#[derive(Serialize, Deserialize)]
struct SignTransactionRequest {
    seed_phrase: String,
    path: String,
    message: String,
}

#[derive(Serialize, Deserialize)]
struct SignTransactionResponse {
    signature: String,
}

#[derive(Serialize, Deserialize)]
struct WalletData {
    balance: f64,
    transactions: Vec<Value>,
}

#[derive(Serialize, Deserialize)]
struct SendTransactionRequestPy {
    token: String,
    recipient: String,
    amount: f64,
}

#[derive(Serialize, Deserialize)]
struct SendTransactionResponsePy {
    success: bool,
    transaction_id: String,
}

#[derive(Serialize, Deserialize)]
struct StrategyInfo {
    name: String,
    author: String,
    description: String,
    parameters: serde_json::Value,
    is_active: bool,
}

#[derive(Serialize, Deserialize)]
struct LoadStrategyRequest {
    token: String,
    file_path: String,
}

#[derive(Serialize, Deserialize)]
struct LoadStrategyResponse {
    success: bool,
    strategy_name: String,
}

#[derive(Serialize, Deserialize)]
struct ActivateStrategyRequest {
    token: String,
    strategy_name: String,
    parameters: serde_json::Value,
}

#[derive(Serialize, Deserialize)]
struct ActivateStrategyResponse {
    success: bool,
    message: String,
}

#[derive(Serialize, Deserialize)]
struct BacktestRequest {
    token: String,
    strategy_name: String,
    symbol: String,
    start_date: String,
    end_date: String,
}

#[derive(Serialize, Deserialize)]
struct BacktestResponse {
    success: bool,
    results: Option<serde_json::Value>,
}

#[derive(Serialize, Deserialize)]
struct ExecuteSignalRequest {
    token: String,
    strategy_name: String,
    signal: serde_json::Value,
}

#[derive(Serialize, Deserialize)]
struct ExecuteSignalResponse {
    success: bool,
    message: String,
    execution_id: Option<String>,
}

#[derive(Serialize, Deserialize)]
struct LLMQueryRequest {
    token: String,
    query: String,
}

#[derive(Serialize, Deserialize)]
struct LLMQueryResponse {
    success: bool,
    response: String,
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // Initialize the key manager
    unsafe {
        KEY_MANAGER = Some(Mutex::new(KeyManager::new()));
    }
    
    tauri::Builder::default()
        .setup(|app| {
            // Start the Python sidecar process
            let sidecar = tauri::command::Command::new_sidecar("python-engine")
                .expect("failed to create `python-engine` binary command");
            
            // Execute the sidecar process
            let output = sidecar
                .output()
                .expect("failed to execute `python-engine` sidecar");
            
            println!("Python engine output: {}", String::from_utf8_lossy(&output.stdout));
            
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            ping_python_engine,
            generate_new_seed,
            import_from_seed,
            derive_private_key_for_path,
            sign_transaction,
            get_wallet_data,
            send_transaction,
            get_strategies,
            load_strategy,
            activate_strategy,
            deactivate_strategy,
            run_backtest,
            execute_signal,
            process_llm_query
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[tauri::command]
async fn ping_python_engine(message: String) -> Result<String, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Create the request payload
    let request = PingRequest {
        token: token.trim().to_string(),
        message,
    };
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .post("http://127.0.0.1:8000/ping")
        .json(&request)
        .send()
        .await
        .map_err(|e| format!("Failed to send request to Python engine: {}", e))?;
    
    // Parse the response
    let response: PingResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response from Python engine: {}", e))?;
    
    Ok(response.message)
}

#[tauri::command]
fn generate_new_seed() -> Result<GenerateSeedResponse, String> {
    unsafe {
        if let Some(ref key_manager) = KEY_MANAGER {
            let key_manager = key_manager.lock().unwrap();
            let seed_phrase = key_manager.generate_new_seed()?;
            Ok(GenerateSeedResponse { seed_phrase })
        } else {
            Err("Key manager not initialized".to_string())
        }
    }
}

#[tauri::command]
fn import_from_seed(request: ImportSeedRequest) -> Result<(), String> {
    unsafe {
        if let Some(ref key_manager) = KEY_MANAGER {
            let key_manager = key_manager.lock().unwrap();
            key_manager.import_from_seed(&request.seed_phrase)
        } else {
            Err("Key manager not initialized".to_string())
        }
    }
}

#[tauri::command]
fn derive_private_key_for_path(request: DeriveKeyRequest) -> Result<DeriveKeyResponse, String> {
    unsafe {
        if let Some(ref key_manager) = KEY_MANAGER {
            let key_manager = key_manager.lock().unwrap();
            let private_key = key_manager.derive_private_key_for_path(&request.seed_phrase, &request.path)?;
            Ok(DeriveKeyResponse { private_key })
        } else {
            Err("Key manager not initialized".to_string())
        }
    }
}

#[tauri::command]
async fn sign_transaction(request: SignTransactionRequest, app_handle: tauri::AppHandle) -> Result<SignTransactionResponse, String> {
    // Show a confirmation dialog to the user
    let confirmed = tauri::dialog::ask(
        Some(&app_handle.get_webview_window("main").unwrap()),
        "Confirm Transaction",
        format!("Do you want to sign this transaction?\n\nMessage: {}", request.message),
    );
    
    if !confirmed {
        return Err("Transaction signing cancelled by user".to_string());
    }
    
    // Perform the signing operation
    unsafe {
        if let Some(ref key_manager) = KEY_MANAGER {
            let key_manager = key_manager.lock().unwrap();
            let signature = key_manager.sign_transaction(&request.seed_phrase, &request.path, &request.message)?;
            Ok(SignTransactionResponse { signature })
        } else {
            Err("Key manager not initialized".to_string())
        }
    }
}

#[tauri::command]
async fn get_wallet_data() -> Result<WalletData, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .get("http://127.0.0.1:8000/wallet/data")
        .header("Authorization", format!("Bearer {}", token.trim()))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch wallet data from Python engine: {}", e))?;
    
    // Parse the response
    let wallet_data: WalletData = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse wallet data from Python engine: {}", e))?;
    
    Ok(wallet_data)
}

#[tauri::command]
async fn send_transaction(recipient: String, amount: f64) -> Result<SendTransactionResponsePy, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Create the request payload
    let request = SendTransactionRequestPy {
        token: token.trim().to_string(),
        recipient,
        amount,
    };
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .post("http://127.0.0.1:8000/wallet/send")
        .json(&request)
        .send()
        .await
        .map_err(|e| format!("Failed to send transaction request to Python engine: {}", e))?;
    
    // Parse the response
    let response: SendTransactionResponsePy = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse transaction response from Python engine: {}", e))?;
    
    Ok(response)
}

#[tauri::command]
async fn get_strategies() -> Result<Vec<StrategyInfo>, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .get("http://127.0.0.1:8000/strategies")
        .header("Authorization", format!("Bearer {}", token.trim()))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch strategies from Python engine: {}", e))?;
    
    // Parse the response
    let strategies: Vec<StrategyInfo> = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse strategies from Python engine: {}", e))?;
    
    Ok(strategies)
}

#[tauri::command]
async fn load_strategy(file_path: String) -> Result<LoadStrategyResponse, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Create the request payload
    let request = LoadStrategyRequest {
        token: token.trim().to_string(),
        file_path,
    };
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .post("http://127.0.0.1:8000/strategies/load")
        .json(&request)
        .send()
        .await
        .map_err(|e| format!("Failed to load strategy on Python engine: {}", e))?;
    
    // Parse the response
    let response: LoadStrategyResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse strategy load response from Python engine: {}", e))?;
    
    Ok(response)
}

#[tauri::command]
async fn activate_strategy(strategy_name: String, parameters: serde_json::Value) -> Result<ActivateStrategyResponse, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Create the request payload
    let request = ActivateStrategyRequest {
        token: token.trim().to_string(),
        strategy_name,
        parameters,
    };
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .post("http://127.0.0.1:8000/strategies/activate")
        .json(&request)
        .send()
        .await
        .map_err(|e| format!("Failed to activate strategy on Python engine: {}", e))?;
    
    // Parse the response
    let response: ActivateStrategyResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse strategy activation response from Python engine: {}", e))?;
    
    Ok(response)
}

#[tauri::command]
async fn deactivate_strategy(strategy_name: String) -> Result<ActivateStrategyResponse, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Create the request payload
    let request = ActivateStrategyRequest {
        token: token.trim().to_string(),
        strategy_name,
        parameters: serde_json::Value::Object(serde_json::Map::new()),
    };
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .post("http://127.0.0.1:8000/strategies/deactivate")
        .json(&request)
        .send()
        .await
        .map_err(|e| format!("Failed to deactivate strategy on Python engine: {}", e))?;
    
    // Parse the response
    let response: ActivateStrategyResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse strategy deactivation response from Python engine: {}", e))?;
    
    Ok(response)
}

#[tauri::command]
async fn run_backtest(strategy_name: String, symbol: String, start_date: String, end_date: String) -> Result<BacktestResponse, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Create the request payload
    let request = BacktestRequest {
        token: token.trim().to_string(),
        strategy_name,
        symbol,
        start_date,
        end_date,
    };
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .post("http://127.0.0.1:8000/strategies/backtest")
        .json(&request)
        .send()
        .await
        .map_err(|e| format!("Failed to run backtest on Python engine: {}", e))?;
    
    // Parse the response
    let response: BacktestResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse backtest response from Python engine: {}", e))?;
    
    Ok(response)
}

#[tauri::command]
async fn execute_signal(strategy_name: String, signal: serde_json::Value) -> Result<ExecuteSignalResponse, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Create the request payload
    let request = ExecuteSignalRequest {
        token: token.trim().to_string(),
        strategy_name,
        signal,
    };
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .post("http://127.0.0.1:8000/strategies/execute")
        .json(&request)
        .send()
        .await
        .map_err(|e| format!("Failed to execute signal on Python engine: {}", e))?;
    
    // Parse the response
    let response: ExecuteSignalResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse signal execution response from Python engine: {}", e))?;
    
    Ok(response)
}

#[tauri::command]
async fn process_llm_query(query: String) -> Result<LLMQueryResponse, String> {
    // Read the secret token from the file
    let token = fs::read_to_string("secret_token.txt")
        .map_err(|e| format!("Failed to read secret token: {}", e))?;
    
    // Create the request payload
    let request = LLMQueryRequest {
        token: token.trim().to_string(),
        query,
    };
    
    // Send the request to the Python engine
    let client = reqwest::Client::new();
    let response = client
        .post("http://127.0.0.1:8000/llm/query")
        .json(&request)
        .send()
        .await
        .map_err(|e| format!("Failed to process LLM query on Python engine: {}", e))?;
    
    // Parse the response
    let response: LLMQueryResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse LLM query response from Python engine: {}", e))?;
    
    Ok(response)
}