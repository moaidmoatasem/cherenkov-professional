import React, { useState } from 'react';
import { Upload, Smartphone, ShieldCheck, AlertCircle } from 'lucide-react';
import { CyberButton } from '../atoms/CyberButton';

export function MobileTargetForm() {
  const [file, setFile] = useState<File | null>(null);
  const [packageName, setPackageName] = useState('');
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setScanning(true);
    const formData = new FormData();
    formData.append('file', file);
    if (packageName) formData.append('package_name', packageName);

    try {
      const response = await fetch('/api/v1/mobile/scan', {
        method: 'POST',
        headers: {
          // Note: Browser will set Content-Type with boundary automatically for FormData
          'Authorization': `Bearer ${localStorage.getItem('cherenkov_token')}`,
        },
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Mobile scan failed:', err);
    } finally {
      setScanning(false);
    }
  };

  return (
    <div className="bg-bg-surface p-6 border border-white/5 hud-bracket flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <Smartphone className="text-hud-cyan" size={24} />
        <h2 className="text-lg font-bold text-white uppercase tracking-wider">Mobile_Triage_Sandbox</h2>
      </div>

      <form onSubmit={handleUpload} className="flex flex-col gap-4">
        <div className="flex flex-col gap-2">
          <label className="text-[10px] font-mono text-fg3 uppercase">Target_Binary (APK/IPA)</label>
          <div className="relative group">
            <input
              type="file"
              accept=".apk,.ipa"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            />
            <div className={`
              border border-dashed p-8 flex flex-col items-center justify-center gap-2 transition-all
              ${file ? 'border-hud-cyan bg-hud-cyan/5' : 'border-white/20 group-hover:border-white/40'}
            `}>
              <Upload size={32} className={file ? 'text-hud-cyan' : 'text-fg3'} />
              <span className="text-[11px] font-mono text-fg3">
                {file ? file.name : 'CLICK_OR_DRAG_TO_detonate_binary'}
              </span>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-[10px] font-mono text-fg3 uppercase">Package_Name (Optional)</label>
          <input
            type="text"
            value={packageName}
            onChange={(e) => setPackageName(e.target.value)}
            placeholder="com.example.app"
            className="bg-black/50 border border-white/10 p-2 text-[12px] font-mono text-white focus:border-hud-cyan outline-none"
          />
        </div>

        <CyberButton
          type="submit"
          variant="primary"
          className="py-3"
          disabled={!file || scanning}
        >
          {scanning ? 'DETONATING_IN_TOKAMAK...' : 'INITIATE_MOBILE_TRIAGE'}
        </CyberButton>
      </form>

      {result && (
        <div className="border-t border-white/10 pt-4 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono text-fg3">SCAN_ID: {result.scan_id}</span>
            <div className="flex items-center gap-1 text-hud-green">
              <ShieldCheck size={14} />
              <span className="text-[10px] font-mono uppercase">Detonation_Complete</span>
            </div>
          </div>

          <div className="flex flex-col gap-2">
            {result.findings.map((finding: any) => (
              <div key={finding.id} className="bg-black/40 border border-white/5 p-3 flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-bold text-white">{finding.title}</span>
                  <span className={`text-[9px] px-1.5 py-0.5 rounded ${
                    finding.severity === 'HIGH' ? 'bg-hud-red/20 text-hud-red' : 'bg-hud-amber/20 text-hud-amber'
                  }`}>
                    {finding.severity}
                  </span>
                </div>
                <span className="text-[10px] font-mono text-fg3">{finding.evidence}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
