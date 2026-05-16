import { useState, useEffect } from 'react';
import { MainLayout } from './components/templates/MainLayout';
import { LoginPage } from './components/templates/LoginPage';
import { ForensicHeader } from './components/organisms/ForensicHeader';
import { TacticalOperationsPanel } from './components/organisms/TacticalOperationsPanel';
import { ThreatIntelPanel } from './components/organisms/ThreatIntelPanel';
import { LogoKit, AssistantWidget } from './components/organisms';
import { MobileDashboard } from './components/templates/MobileDashboard';
import { AnimatePresence } from 'motion/react';

export default function App() {
  const [token, setToken] = useState<string | null>(sessionStorage.getItem('cherenkov_token'));
  const [showLogoKit, setShowLogoKit] = useState(false);
  const [view, setView] = useState<'tactical' | 'mobile'>('tactical');

  if (!token) {
    return <LoginPage onLoginSuccess={setToken} />;
  }

  return (
    <>
      {view === 'tactical' ? (
        <MainLayout 
          header={<ForensicHeader />}
          content={<TacticalOperationsPanel />}
          sidebar={<ThreatIntelPanel />}
        />
      ) : (
        <MobileDashboard />
      )}

      {/* View Switcher Overlay (Temporary until Header integration) */}
      <div className="fixed bottom-4 left-4 flex gap-2 z-50">
        <button 
          onClick={() => setView('tactical')}
          className={`px-3 py-1 text-[10px] font-mono border ${view === 'tactical' ? 'bg-hud-cyan text-black border-hud-cyan' : 'bg-black text-hud-cyan border-hud-cyan/40'}`}
        >
          TACTICAL
        </button>
        <button 
          onClick={() => setView('mobile')}
          className={`px-3 py-1 text-[10px] font-mono border ${view === 'mobile' ? 'bg-hud-cyan text-black border-hud-cyan' : 'bg-black text-hud-cyan border-hud-cyan/40'}`}
        >
          MOBILE_TRIAGE
        </button>
      </div>

      {/* Legacy LogoKit Support (updated check) */}
      <AnimatePresence>
        {showLogoKit && <LogoKit onClose={() => setShowLogoKit(false)} />}
      </AnimatePresence>

      {/* Global LogoKit Trigger Keyboard Shortcut */}
      <LogoKitTrigger onTrigger={() => setShowLogoKit(true)} />

      {/* AI Studio Assistant Integration */}
      <AssistantWidget />
    </>
  );
}

// Hidden utility to trigger logo kit if needed (e.g. for developer review)
function LogoKitTrigger({ onTrigger }: { onTrigger: () => void }) {
  // We can also just add a button in the UI if needed, but for now we follow the spec
  // which might have removed the explicit button in the new header.
  // I'll add a small hidden button or just let it be for now.
  return (
    <button 
      onClick={onTrigger}
      className="fixed bottom-2 right-2 w-4 h-4 bg-white/5 hover:bg-white/10 rounded-full z-[1000] opacity-0 hover:opacity-100 transition-opacity"
      title="Open Design Kit"
    />
  );
}


