import React from 'react';
import { MainLayout } from './MainLayout';
import { MobileTargetForm, MobileResultsPanel, ForensicHeader, ThreatIntelPanel } from '../organisms';
import { Smartphone, LayoutDashboard, Activity, Database } from 'lucide-react';

export function MobileDashboard() {
  const content = (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <header className="flex items-center justify-between border-b border-white/5 pb-4">
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-2">
              <Smartphone className="text-hud-cyan" size={18} />
              <h1 className="text-xl font-bold text-white uppercase tracking-tighter">Mobile_Triage_Center</h1>
            </div>
            <p className="text-[10px] font-mono text-fg3 uppercase tracking-widest">Phase_4_Hardening_Subsystem // Alpha_v0.1</p>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex flex-col items-end">
              <span className="text-[10px] font-mono text-fg3 uppercase">Sandbox_Status</span>
              <span className="text-[12px] font-bold text-hud-green uppercase">Operational</span>
            </div>
            <div className="h-8 w-px bg-white/10" />
            <div className="flex flex-col items-end">
              <span className="text-[10px] font-mono text-fg3 uppercase">Active_Simulations</span>
              <span className="text-[12px] font-bold text-white uppercase">04</span>
            </div>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column - Target & Controls */}
          <div className="lg:col-span-5 flex flex-col gap-6">
            <MobileTargetForm />
            
            <div className="bg-black/40 border border-white/5 p-4 flex flex-col gap-3">
              <div className="flex items-center gap-2">
                <Database size={14} className="text-hud-cyan" />
                <span className="text-[10px] font-mono text-white uppercase">Historical_Triages</span>
              </div>
              <div className="flex flex-col gap-2">
                {[
                  { name: 'app-release.apk', date: '2024-05-16', findings: 2 },
                  { name: 'banking_v4.ipa', date: '2024-05-15', findings: 12 },
                  { name: 'payload_debug.apk', date: '2024-05-14', findings: 0 },
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-2 hover:bg-white/5 transition-colors group cursor-pointer border border-transparent hover:border-white/10">
                    <div className="flex flex-col">
                      <span className="text-[11px] text-white group-hover:text-hud-cyan transition-colors">{item.name}</span>
                      <span className="text-[9px] font-mono text-fg3">{item.date}</span>
                    </div>
                    <span className={`text-[10px] font-mono ${item.findings > 5 ? 'text-hud-red' : 'text-fg3'}`}>
                      {item.findings} FINDINGS
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Telemetry & Deep Analysis */}
          <div className="lg:col-span-7">
            <MobileResultsPanel />
          </div>
        </div>

        {/* Footer Metrics */}
        <footer className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-4">
          {[
            { label: 'CWE_COVERAGE', value: '82%', icon: Shield },
            { label: 'DETONATION_AVG', value: '42.8s', icon: Activity },
            { label: 'TOKAMAK_LOAD', value: '14.2%', icon: LayoutDashboard },
            { label: 'MOBILE_NODES', value: '03 ACTIVE', icon: Smartphone },
          ].map((stat, i) => (
            <div key={i} className="bg-bg-surface p-3 border border-white/5 flex items-center justify-between">
              <div className="flex flex-col">
                <span className="text-[9px] font-mono text-fg3 uppercase">{stat.label}</span>
                <span className="text-[14px] font-bold text-white">{stat.value}</span>
              </div>
              <stat.icon size={20} className="text-white/10" />
            </div>
          ))}
        </footer>
      </div>
  );

  return (
    <MainLayout 
      header={<ForensicHeader />}
      content={content}
      sidebar={<ThreatIntelPanel />}
    />
  );
}

// Simple Shield icon for the footer
function Shield(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" />
    </svg>
  );
}
