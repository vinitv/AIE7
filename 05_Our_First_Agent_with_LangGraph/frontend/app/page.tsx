'use client';

import { useState, useEffect } from 'react';
import { Rocket, Search, Image, Database, Send, Loader2, Sparkles, Settings } from 'lucide-react';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { getApiBaseUrl, API_ENDPOINTS } from '../lib/config';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  tool?: string;
}

// Custom markdown components for better styling
const MarkdownComponents = {
  // Style headings
  h1: ({ children }: any) => (
    <h1 className="text-2xl font-bold text-white mb-4">{children}</h1>
  ),
  h2: ({ children }: any) => (
    <h2 className="text-xl font-bold text-white mb-3">{children}</h2>
  ),
  h3: ({ children }: any) => (
    <h3 className="text-lg font-semibold text-white mb-2">{children}</h3>
  ),
  
  // Style paragraphs
  p: ({ children }: any) => (
    <p className="text-white/90 mb-3 leading-relaxed">{children}</p>
  ),
  
  // Style links
  a: ({ href, children }: any) => (
    <a 
      href={href} 
      target="_blank" 
      rel="noopener noreferrer"
      className="text-space-400 hover:text-space-300 underline transition-colors"
    >
      {children}
    </a>
  ),
  
  // Style images with proper loading and error handling
  img: ({ src, alt }: any) => (
    <div className="my-4">
      <img 
        src={src} 
        alt={alt} 
        className="max-w-full h-auto rounded-lg border border-white/20 shadow-lg"
        onError={(e) => {
          const target = e.target as HTMLImageElement;
          target.style.display = 'none';
        }}
        onLoad={(e) => {
          const target = e.target as HTMLImageElement;
          target.style.opacity = '1';
        }}
        style={{ opacity: 0, transition: 'opacity 0.3s ease-in-out' }}
      />
      {alt && (
        <p className="text-sm text-white/60 mt-2 italic text-center">{alt}</p>
      )}
    </div>
  ),
  
  // Style lists
  ul: ({ children }: any) => (
    <ul className="list-disc list-inside text-white/90 mb-3 space-y-1">{children}</ul>
  ),
  ol: ({ children }: any) => (
    <ol className="list-decimal list-inside text-white/90 mb-3 space-y-1">{children}</ol>
  ),
  li: ({ children }: any) => (
    <li className="text-white/90">{children}</li>
  ),
  
  // Style code blocks
  code: ({ inline, children }: any) => (
    inline ? (
      <code className="bg-white/10 text-space-300 px-1 py-0.5 rounded text-sm font-mono">
        {children}
      </code>
    ) : (
      <pre className="bg-white/10 text-white/90 p-3 rounded-lg overflow-x-auto mb-3">
        <code className="font-mono text-sm">{children}</code>
      </pre>
    )
  ),
  
  // Style blockquotes
  blockquote: ({ children }: any) => (
    <blockquote className="border-l-4 border-space-400 pl-4 text-white/80 italic mb-3">
      {children}
    </blockquote>
  ),
  
  // Style strong/bold text
  strong: ({ children }: any) => (
    <strong className="font-bold text-white">{children}</strong>
  ),
  
  // Style emphasis/italic text
  em: ({ children }: any) => (
    <em className="italic text-white/90">{children}</em>
  ),
};

export default function Home() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [apiKeysConfigured, setApiKeysConfigured] = useState(false);
  const [checkingKeys, setCheckingKeys] = useState(true);
  const router = useRouter();

  // Check if API keys are configured on component mount
  useEffect(() => {
    const checkAPIKeys = () => {
      const storedKeys = localStorage.getItem('space_agent_api_keys');
      
      if (storedKeys) {
        try {
          const keys = JSON.parse(storedKeys);
          if (keys.openai && keys.tavily) {
            setApiKeysConfigured(true);
          }
        } catch (e) {
          console.error('Failed to parse stored keys');
        }
      }
      
      setCheckingKeys(false);
    };

    checkAPIKeys();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: question.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setQuestion('');
    setIsLoading(true);

    try {
      // Use configured API keys
      const storedKeys = localStorage.getItem('space_agent_api_keys');
      if (!storedKeys) {
        throw new Error('No API keys configured');
      }
      
      const keys = JSON.parse(storedKeys);
      const apiBaseUrl = getApiBaseUrl();
      const response = await axios.post(`${apiBaseUrl}${API_ENDPOINTS.ASK}`, {
        question: question.trim(),
        openai_key: keys.openai,
        tavily_key: keys.tavily,
        nasa_key: keys.nasa || 'DEMO_KEY',
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.data.answer,
        timestamp: new Date(),
        tool: response.data.tools_used,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error asking question:', error);
      
      // Extract error message from different error formats
      let errorContent = 'Sorry, I encountered an error while processing your question. Please check your API keys and try again.';
      
      if (axios.isAxiosError(error)) {
        if (error.response?.data?.detail) {
          // FastAPI HTTPException format
          errorContent = `Error: ${error.response.data.detail}`;
        } else if (error.response?.data?.message) {
          // Standard error message format
          errorContent = `Error: ${error.response.data.message}`;
        } else if (error.message) {
          // Axios error message
          errorContent = `Network Error: ${error.message}`;
        }
      } else if (error instanceof Error) {
        // Standard JavaScript Error
        errorContent = `Error: ${error.message}`;
      } else if (typeof error === 'string') {
        // String error
        errorContent = `Error: ${error}`;
      }
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: errorContent,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const exampleQuestions = [
    "What are the latest developments in Mars exploration?",
    "Generate an image of a futuristic space station orbiting Earth",
    "What's the latest astronomy picture of the day from NASA?",
    "Tell me about the James Webb Space Telescope discoveries",
    "What asteroids are near Earth right now?",
    "Create an image of a black hole with accretion disk",
  ];

  const handleExampleClick = (example: string) => {
    if (!apiKeysConfigured) {
      router.push('/setup');
      return;
    }
    
    setQuestion(example);
  };

  // Show loading state while checking API keys
  if (checkingKeys) {
    return (
      <div className="min-h-screen p-4 md:p-8 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-space-400" />
            <p className="text-white/80">Checking configuration...</p>
          </div>
        </div>
      </div>
    );
  }

  // Show setup prompt if API keys are not configured
  if (!apiKeysConfigured) {
    return (
      <div className="min-h-screen p-4 md:p-8 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <Rocket className="w-8 h-8 text-space-400" />
              <h1 className="text-4xl md:text-6xl font-bold text-white">
                Space Exploration Agent
              </h1>
              <Sparkles className="w-8 h-8 text-space-400" />
            </div>
            <p className="text-xl text-white/80 max-w-2xl mx-auto">
              Your AI-powered research assistant for space exploration and astronomy. 
              Ask questions, generate space images, and explore the cosmos!
            </p>
          </div>

          {/* Setup Card */}
          <div className="space-card p-8 text-center">
            <Rocket className="w-16 h-16 mx-auto mb-6 text-space-400" />
            <h2 className="text-2xl font-bold text-white mb-4">
              Ready to Explore the Cosmos?
            </h2>
            <p className="text-white/70 mb-8 max-w-lg mx-auto">
              To get started, you'll need to configure your API keys for OpenAI, Tavily, and NASA. 
              Don't worry - we store everything locally in your browser.
            </p>
            
            <div className="space-y-4 max-w-md mx-auto">
              <button
                onClick={() => router.push('/setup')}
                className="w-full cosmic-button text-lg py-4"
              >
                Configure API Keys
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex">
      {/* Left Sidebar */}
      <div className="w-80 bg-black/30 backdrop-blur-sm border-r border-white/10 p-6 flex flex-col">
        {/* Header */}
        <div className="text-center space-y-4 mb-8">
          <div className="flex items-center justify-center space-x-2">
            <Rocket className="w-6 h-6 text-space-400" />
            <h1 className="text-xl font-bold text-white">
              Space Agent
            </h1>
            <Sparkles className="w-6 h-6 text-space-400" />
          </div>
          <button
            onClick={() => router.push('/setup')}
            className="flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white/80 hover:text-white rounded-lg transition-colors border border-white/20 w-full justify-center"
          >
            <Settings className="w-4 h-4" />
            <span>Settings</span>
          </button>
        </div>

        {/* Tools Info */}
        <div className="space-y-4 mb-8">
          <h3 className="text-lg font-semibold text-white mb-4">Available Tools</h3>
          
          <div className="space-card p-4">
            <div className="flex items-center space-x-3 mb-2">
              <Search className="w-5 h-5 text-space-400" />
              <h4 className="text-sm font-semibold text-white">Web Search</h4>
            </div>
            <p className="text-xs text-white/70">
              Latest space news and research
            </p>
          </div>
          
          <div className="space-card p-4">
            <div className="flex items-center space-x-3 mb-2">
              <Image className="w-5 h-5 text-space-400" />
              <h4 className="text-sm font-semibold text-white">DALL-E Images</h4>
            </div>
            <p className="text-xs text-white/70">
              Generate space visualizations
            </p>
          </div>
          
          <div className="space-card p-4">
            <div className="flex items-center space-x-3 mb-2">
              <Database className="w-5 h-5 text-space-400" />
              <h4 className="text-sm font-semibold text-white">NASA Data</h4>
            </div>
            <p className="text-xs text-white/70">
              Official NASA data and images
            </p>
          </div>
        </div>

        {/* Example Questions */}
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-4">Try these examples:</h3>
          <div className="space-y-2">
            {exampleQuestions.map((example, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(example)}
                className="text-left p-3 rounded-lg bg-white/5 hover:bg-white/10 text-white/80 hover:text-white transition-colors border border-white/10 hover:border-white/20 w-full text-sm"
                disabled={isLoading}
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="text-xs text-white/60">
            Powered by LangGraph, OpenAI, and NASA APIs
          </p>
        </div>
      </div>

      {/* Main Chat Interface */}
      <div className="flex-1 flex flex-col p-6">
        <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-white mb-2">Space Exploration Assistant</h2>
            <p className="text-white/70">Ask questions, generate images, and explore the cosmos!</p>
          </div>
          
          <div className="space-card p-6 mb-6 flex-1 flex flex-col">
            {/* Messages */}
            <div className="space-y-4 mb-6 flex-1 overflow-y-auto">
            {messages.length === 0 ? (
              <div className="text-center text-white/60 py-8">
                <Rocket className="w-12 h-12 mx-auto mb-4 text-space-400" />
                <p>Start exploring the cosmos by asking a question!</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-4 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-space-600 text-white'
                        : 'bg-white/10 text-white border border-white/20'
                    }`}
                  >
                    {message.type === 'user' ? (
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    ) : (
                      <div className="prose prose-invert max-w-none">
                        <ReactMarkdown 
                          components={MarkdownComponents}
                          remarkPlugins={[remarkGfm]}
                        >
                          {message.content}
                        </ReactMarkdown>
                      </div>
                    )}
                    <div className="flex justify-between items-center mt-2">
                      <p className="text-xs opacity-60">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                      {message.tool && message.type === 'assistant' && (
                        <p className="text-xs opacity-50 italic">
                          via {message.tool}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white/10 text-white border border-white/20 rounded-lg p-4">
                  <div className="flex items-center space-x-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Exploring the cosmos...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="flex space-x-4">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask about space exploration, request images, or get NASA data..."
              className="stellar-input flex-1"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !question.trim()}
              className="cosmic-button disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
  );
} 