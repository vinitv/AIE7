'use client';

import { useState, useEffect } from 'react';
import { Rocket, Key, Eye, EyeOff, CheckCircle, AlertCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface APIKeys {
  openai: string;
  tavily: string;
  nasa: string;
}

export default function SetupPage() {
  const [apiKeys, setApiKeys] = useState<APIKeys>({
    openai: '',
    tavily: '',
    nasa: '',
  });
  const [showKeys, setShowKeys] = useState<{ [key: string]: boolean }>({
    openai: false,
    tavily: false,
    nasa: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const router = useRouter();

  const handleInputChange = (key: keyof APIKeys, value: string) => {
    setApiKeys(prev => ({ ...prev, [key]: value }));
    setError('');
  };

  const toggleKeyVisibility = (key: string) => {
    setShowKeys(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const validateKeys = async () => {
    setIsLoading(true);
    setError('');
    setSuccess(false);

    try {
      // Basic validation - check if required keys are provided
      if (!apiKeys.openai.trim()) {
        setError('OpenAI API key is required');
        return;
      }
      
      if (!apiKeys.tavily.trim()) {
        setError('Tavily API key is required');
        return;
      }

      // Store keys in localStorage (in production, you'd want to encrypt these)
      localStorage.setItem('space_agent_api_keys', JSON.stringify(apiKeys));
      
      setSuccess(true);
      setTimeout(() => {
        router.push('/');
      }, 2000);
    } catch (err) {
      setError('Failed to save API keys. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getKeyFromStorage = () => {
    const stored = localStorage.getItem('space_agent_api_keys');
    if (stored) {
      try {
        const keys = JSON.parse(stored);
        setApiKeys(keys);
      } catch (e) {
        console.error('Failed to parse stored keys');
      }
    }
  };

  // Load stored keys on component mount
  useEffect(() => {
    getKeyFromStorage();
  }, []);

  return (
    <div className="min-h-screen p-4 md:p-8 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <Rocket className="w-8 h-8 text-space-400" />
            <h1 className="text-3xl md:text-4xl font-bold text-white">
              Setup Space Exploration Agent
            </h1>
          </div>
          <p className="text-lg text-white/80">
            Enter your API keys to get started with your AI-powered space exploration assistant
          </p>
        </div>

        {/* Setup Form */}
        <div className="space-card p-8">
          <div className="space-y-6">
            {/* OpenAI API Key */}
            <div>
              <label className="block text-white font-semibold mb-2">
                OpenAI API Key *
              </label>
              <div className="relative">
                <input
                  type={showKeys.openai ? 'text' : 'password'}
                  value={apiKeys.openai}
                  onChange={(e) => handleInputChange('openai', e.target.value)}
                  placeholder="sk-..."
                  className="stellar-input w-full pr-12"
                />
                <button
                  type="button"
                  onClick={() => toggleKeyVisibility('openai')}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/60 hover:text-white"
                >
                  {showKeys.openai ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <p className="text-sm text-white/60 mt-1">
                Required for GPT-4 reasoning and DALL-E image generation
              </p>
            </div>

            {/* Tavily API Key */}
            <div>
              <label className="block text-white font-semibold mb-2">
                Tavily API Key *
              </label>
              <div className="relative">
                <input
                  type={showKeys.tavily ? 'text' : 'password'}
                  value={apiKeys.tavily}
                  onChange={(e) => handleInputChange('tavily', e.target.value)}
                  placeholder="tvly-..."
                  className="stellar-input w-full pr-12"
                />
                <button
                  type="button"
                  onClick={() => toggleKeyVisibility('tavily')}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/60 hover:text-white"
                >
                  {showKeys.tavily ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <p className="text-sm text-white/60 mt-1">
                Required for web search capabilities
              </p>
            </div>

            {/* NASA API Key */}
            <div>
              <label className="block text-white font-semibold mb-2">
                NASA API Key (Optional)
              </label>
              <div className="relative">
                <input
                  type={showKeys.nasa ? 'text' : 'password'}
                  value={apiKeys.nasa}
                  onChange={(e) => handleInputChange('nasa', e.target.value)}
                  placeholder="DEMO_KEY or your NASA API key"
                  className="stellar-input w-full pr-12"
                />
                <button
                  type="button"
                  onClick={() => toggleKeyVisibility('nasa')}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/60 hover:text-white"
                >
                  {showKeys.nasa ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <p className="text-sm text-white/60 mt-1">
                Optional. Uses DEMO_KEY if not provided. Get one at <a href="https://api.nasa.gov/" target="_blank" rel="noopener noreferrer" className="text-space-400 hover:underline">api.nasa.gov</a>
              </p>
            </div>

            {/* Error/Success Messages */}
            {error && (
              <div className="flex items-center space-x-2 p-4 bg-red-500/20 border border-red-500/30 rounded-lg">
                <AlertCircle className="w-5 h-5 text-red-400" />
                <span className="text-red-300">{error}</span>
              </div>
            )}

            {success && (
              <div className="flex items-center space-x-2 p-4 bg-green-500/20 border border-green-500/30 rounded-lg">
                <CheckCircle className="w-5 h-5 text-green-400" />
                <span className="text-green-300">API keys validated successfully! Redirecting...</span>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-4 pt-4">
              <button
                onClick={validateKeys}
                disabled={isLoading || !apiKeys.openai || !apiKeys.tavily}
                className="cosmic-button disabled:opacity-50 disabled:cursor-not-allowed flex-1"
              >
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>Validating...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Key className="w-5 h-5" />
                    <span>Validate & Continue</span>
                  </div>
                )}
              </button>

              <button
                onClick={() => router.push('/')}
                className="px-6 py-3 border border-white/20 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
              >
                Skip for Now
              </button>
            </div>
          </div>
        </div>

        {/* Help Section */}
        <div className="space-card p-6 mt-6">
          <h3 className="text-lg font-semibold text-white mb-4">How to get API keys:</h3>
          <div className="space-y-3 text-sm text-white/70">
            <div>
              <strong className="text-white">OpenAI API Key:</strong>
              <ol className="list-decimal list-inside ml-4 mt-1 space-y-1">
                <li>Go to <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-space-400 hover:underline">platform.openai.com/api-keys</a></li>
                <li>Sign in or create an account</li>
                <li>Click "Create new secret key"</li>
                <li>Copy the key (starts with "sk-")</li>
              </ol>
            </div>
            <div>
              <strong className="text-white">Tavily API Key:</strong>
              <ol className="list-decimal list-inside ml-4 mt-1 space-y-1">
                <li>Go to <a href="https://tavily.com/" target="_blank" rel="noopener noreferrer" className="text-space-400 hover:underline">tavily.com</a></li>
                <li>Sign up for a free account</li>
                <li>Get your API key from the dashboard</li>
                <li>Copy the key (starts with "tvly-")</li>
              </ol>
            </div>
            <div>
              <strong className="text-white">NASA API Key (Optional):</strong>
              <ol className="list-decimal list-inside ml-4 mt-1 space-y-1">
                <li>Go to <a href="https://api.nasa.gov/" target="_blank" rel="noopener noreferrer" className="text-space-400 hover:underline">api.nasa.gov</a></li>
                <li>Fill out the form to get a free API key</li>
                <li>Or use "DEMO_KEY" for limited access</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 