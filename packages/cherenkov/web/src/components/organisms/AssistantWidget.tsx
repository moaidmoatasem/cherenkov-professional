import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { CyberButton } from '../atoms';
import { MessageSquare, X } from 'lucide-react';

export function AssistantWidget() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-[1000] flex flex-col items-end gap-4">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            className="w-[400px] h-[600px] max-h-[80vh] bg-cherenkov-surface/90 backdrop-blur-md border border-cherenkov-primary/30 rounded-xl overflow-hidden shadow-[0_0_40px_rgba(0,0,0,0.5)] flex flex-col"
          >
            <div className="flex items-center justify-between px-4 py-3 bg-cherenkov-surface border-b border-cherenkov-primary/20">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-cherenkov-primary animate-pulse shadow-[0_0_8px_theme(colors.cherenkov.primary)]" />
                <h3 className="text-sm font-semibold text-cherenkov-text tracking-wide">AI Security Assistant</h3>
              </div>
              <button 
                onClick={() => setIsOpen(false)}
                className="p-1 rounded-md text-cherenkov-muted hover:text-cherenkov-text hover:bg-white/5 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="flex-1 w-full bg-cherenkov-background relative">
              <iframe
                src="https://ais-dev-wnzpmrbfgr356tzt6nhup2-59657545691.europe-west2.run.app"
                className="absolute inset-0 w-full h-full border-0"
                allow="microphone; camera"
                title="Cherenkov AI Assistant"
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <CyberButton
        onClick={() => setIsOpen(!isOpen)}
        variant="primary"
        className="w-14 h-14 !p-0 !rounded-full flex items-center justify-center shadow-[0_0_20px_theme(colors.cherenkov.primary/0.5)] hover:shadow-[0_0_30px_theme(colors.cherenkov.primary/0.8)]"
      >
        {isOpen ? <X className="w-6 h-6" /> : <MessageSquare className="w-6 h-6" />}
      </CyberButton>
    </div>
  );
}
