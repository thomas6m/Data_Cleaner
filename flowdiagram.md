# 🔄 Data Cleaner - System Architecture & Flow

## 📊 Main Processing Flow

```mermaid
flowchart TD
    A[📁 Input File] --> B{🔍 Entry Method}
    B -->|CLI| C[🖥️ cli.py]
    B -->|Library| D[🐍 DataCleaner Class]
    
    C --> E[⚙️ Parse Arguments]
    E --> F[✅ Validate Parameters]
    F --> G[🚀 Initialize DataCleaner]
    
    D --> G
    G --> H[📈 Performance Tracker]
    H --> I[🔍 File Validation]
    
    I --> J{📂 File Format}
    J -->|CSV| K[📄 Direct Processing]
    J -->|Excel| L[📊 Excel Converter]
    J -->|JSON| M[📋 JSON Converter]
    J -->|TSV/TXT| N[📝 Text Converter]
    J -->|Parquet| O[🗃️ Parquet Handler]
    
    L --> P[🔄 converter.py]
    M --> P
    N --> P
    O --> P
    K --> Q[💾 Memory Check]
    P --> Q
    
    Q --> R{🧠 Memory Safe?}
    R -->|No| S[⚠️ Large File Warning]
    R -->|Yes| T[🧹 Data Cleaning]
    S --> U[💡 Streaming Suggestion]
    U --> T
    
    T --> V[📋 Header Validation]
    V --> W[🏷️ Column Normalization]
    W --> X[🔍 Missing Column Check]
    
    X --> Y{❓ Missing Columns}
    Y -->|Yes| Z[🎯 Fuzzy Matching]
    Y -->|No| AA[✨ Quality Check]
    
    Z --> BB[💡 Smart Suggestions]
    BB --> CC[👤 User Decision]
    CC --> AA
    
    AA --> DD[📊 Performance Logging]
    DD --> EE[💾 CSV Output]
    EE --> FF[✅ Success/Error]
    
    FF --> GG[📈 Performance Report]
    GG --> HH[🎉 Complete]
```

## 🏗️ Component Architecture

```mermaid
graph TB
    subgraph "🎯 Core Components"
        A[cli.py<br/>CLI Interface]
        B[DataCleaner<br/>Main Class]
        C[converter.py<br/>Format Conversion]
    end
    
    subgraph "🛠️ Utilities"
        D[utils.py<br/>Validation & Suggestions]
        E[perf_utils.py<br/>Performance Tracking]
        F[logger_setup.py<br/>Centralized Logging]
    end
    
    subgraph "⚙️ Configuration"
        G[config.py<br/>Global Constants]
        H[lookup.py<br/>Column Mappings]
    end
    
    subgraph "📁 Supported Formats"
        I[📄 CSV Files]
        J[📊 Excel Files]
        K[📋 JSON/JSONL]
        L[📝 TSV/TXT]
        M[🗃️ Parquet]
    end
    
    A --> B
    B --> C
    B --> D
    B --> E
    A --> F
    C --> D
    E --> F
    G -.-> B
    H -.-> D
    
    I --> C
    J --> C
    K --> C
    L --> C
    M --> C
```

## 🔄 Error Handling Flow

```mermaid
flowchart TD
    A[❌ Error Detected] --> B{🔍 Error Type}
    
    B -->|File Not Found| C[📂 FileNotFoundError]
    B -->|Permission| D[🔒 PermissionError]
    B -->|Format| E[📋 ValueError]
    B -->|Memory| F[🧠 RuntimeError]
    B -->|Encoding| G[🔤 UnicodeError]
    
    C --> H[💡 Path Suggestions]
    D --> I[🔓 Access Solutions]
    E --> J[📊 Format Support Info]
    F --> K[⚡ Memory Optimization]
    G --> L[🌐 Encoding Detection]
    
    H --> M[📝 Detailed Error Message]
    I --> M
    J --> M
    K --> M
    L --> M
    
    M --> N[🎯 Smart Suggestions]
    N --> O[👤 User Guidance]
```

## 📈 Performance Monitoring

```mermaid
sequenceDiagram
    participant U as User
    participant DC as DataCleaner
    participant PT as PerformanceTracker
    participant MM as MemoryMonitor
    
    U->>DC: Process File
    DC->>PT: Start Tracking
    PT->>MM: Begin Memory Monitor
    
    loop Processing Steps
        DC->>PT: Log Step Start
        DC->>DC: Execute Operation
        MM->>PT: Memory Usage Update
        DC->>PT: Log Step Complete
    end
    
    PT->>MM: Stop Monitoring
    PT->>DC: Generate Report
    DC->>U: Results + Performance Summary
```

## 🎯 Usage Patterns

### CLI Usage Flow
```mermaid
flowchart LR
    A[📝 Command Input] --> B[⚙️ Argument Parsing]
    B --> C[✅ Validation]
    C --> D[🚀 Processing]
    D --> E[📊 Results]
    E --> F[📈 Performance Report]
```

### Library Usage Flow
```mermaid
flowchart LR
    A[🐍 Python Import] --> B[🏗️ DataCleaner Init]
    B --> C[📁 File Processing]
    C --> D[🔄 Method Calls]
    D --> E[📊 Results Object]
```

---

## 📚 How to Use This Diagram

1. **Copy the markdown content** above
2. **Paste it into your README.md** in the appropriate section
3. **GitHub will automatically render** the Mermaid diagrams
4. **Customize colors/styling** by modifying the mermaid syntax if needed

## 🎨 Diagram Features

- ✅ **GitHub Compatible**: Uses Mermaid syntax supported by GitHub
- 🎯 **Clear Visual Hierarchy**: Different shapes and colors for different components
- 📱 **Mobile Friendly**: Scales well on different screen sizes
- 🔄 **Interactive**: Hover effects and clickable elements (when supported)
- 📊 **Comprehensive**: Shows main flow, architecture, error handling, and performance monitoring

## 💡 Pro Tips for GitHub

- Mermaid diagrams render automatically in GitHub README files
- No additional setup or external tools required
- Diagrams are searchable and accessible
- They automatically adapt to GitHub's light/dark themes
- Can be easily updated by editing the markdown source