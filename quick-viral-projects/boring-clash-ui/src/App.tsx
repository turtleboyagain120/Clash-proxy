import { useState } from 'react'
import yaml from 'yaml'

function App() {
  const [config, setConfig] = useState('')
  const [proxies, setProxies] = useState([])

  const loadConfig = () => {
    const parsed = yaml.parse(config)
    setProxies(parsed.proxies || [])
  }

  return (
    <div style={{padding: '20px'}}>
      <h1>Boring Clash UI</h1>
      <textarea 
        value={config} 
        onChange={(e) => setConfig(e.target.value)}
        placeholder="Paste Clash YAML config"
        rows={10} cols={80}
      />
      <br/>
      <button onClick={loadConfig}>Load Proxies</button>
      <ul>
        {proxies.map((p: any, i) => (
          <li key={i}>{p.name} - {p.type}</li>
        ))}
      </ul>
    </div>
  )
}

export default App

