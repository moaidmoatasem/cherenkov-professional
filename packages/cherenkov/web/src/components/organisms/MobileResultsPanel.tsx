import { Shield, Lock, FileCode, Zap } from 'lucide-react';

interface MobileResultsPanelProps {
  findings?: any[];
}

export function MobileResultsPanel({ findings = [] }: MobileResultsPanelProps) {
  return (
    <div className="bg-bg-surface p-6 border border-white/5 hud-bracket h-full flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <Shield className="text-hud-amber" size={24} />
        <h2 className="text-lg font-bold text-white uppercase tracking-wider">Mobile_Security_Telemetry</h2>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-black/30 p-4 border border-white/5 flex flex-col gap-2">
          <div className="flex items-center gap-2 text-hud-cyan">
            <Lock size={14} />
            <span className="text-[10px] font-mono uppercase tracking-widest">Permissions</span>
          </div>
          <div className="flex flex-col gap-1">
            {['INTERNET', 'READ_EXTERNAL_STORAGE', 'CAMERA', 'LOCATION'].map(p => (
              <span key={p} className="text-[11px] text-fg3 font-mono">android.permission.{p}</span>
            ))}
          </div>
        </div>

        <div className="bg-black/30 p-4 border border-white/5 flex flex-col gap-2">
          <div className="flex items-center gap-2 text-hud-green">
            <Zap size={14} />
            <span className="text-[10px] font-mono uppercase tracking-widest">Binary_Flags</span>
          </div>
          <div className="flex flex-col gap-1">
            <div className="flex justify-between text-[11px] font-mono">
              <span className="text-fg3">PIE</span>
              <span className="text-hud-green">ENABLED</span>
            </div>
            <div className="flex justify-between text-[11px] font-mono">
              <span className="text-fg3">ARC</span>
              <span className="text-hud-green">ENABLED</span>
            </div>
            <div className="flex justify-between text-[11px] font-mono">
              <span className="text-fg3">Canary</span>
              <span className="text-hud-red">DISABLED</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 flex flex-col gap-3 overflow-hidden">
        <div className="flex items-center gap-2 text-fg3 border-b border-white/10 pb-2">
          <FileCode size={14} />
          <span className="text-[10px] font-mono uppercase tracking-widest">Detailed_Findings</span>
        </div>
        
        <div className="flex-1 overflow-y-auto custom-scrollbar flex flex-col gap-2 pr-2">
          {findings.length > 0 ? (
            findings.map((f, i) => (
              <div key={i} className="p-3 bg-hud-red/5 border-l-2 border-hud-red flex flex-col gap-1">
                <span className="text-[11px] font-bold text-white">{f.title}</span>
                <p className="text-[10px] text-fg3 leading-relaxed">{f.evidence}</p>
              </div>
            ))
          ) : (
            <div className="flex flex-col items-center justify-center h-full opacity-20 py-12">
              <Shield size={48} className="text-fg3 mb-4" />
              <span className="text-[10px] font-mono uppercase">Waiting_for_triage_data...</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
