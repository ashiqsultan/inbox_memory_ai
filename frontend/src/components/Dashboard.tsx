import { useNavigate } from 'react-router';
import { useState, useEffect } from 'react';
import { emailAPI } from '../services/api';
import EmailModal from './EmailModal';

interface EmailContent {
  id: string;
  user_id: string;
  subject: string;
  content_html: string;
  content_text: string;
  created_at: string;
}

interface Email {
  id: string;
  subject: string;
  created_at: string;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [emails, setEmails] = useState<Email[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<EmailContent | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [emailLoading, setEmailLoading] = useState(false);
  
  // AI Question states
  const [question, setQuestion] = useState('');
  const [aiAnswer, setAiAnswer] = useState('');
  const [isAskingAI, setIsAskingAI] = useState(false);
  const [showAIAnswer, setShowAIAnswer] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  const fetchEmails = async () => {
    try {
      setLoading(true);
      const response = await emailAPI.getEmailList();
      setEmails(response.emails || []);
    } catch (error) {
      console.error('Error fetching emails:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEmailClick = async (emailId: string) => {
    try {
      setEmailLoading(true);
      const emailContent = await emailAPI.getEmailById(emailId);
      setSelectedEmail(emailContent);
      setIsModalOpen(true);
    } catch (error) {
      console.error('Error fetching email content:', error);
    } finally {
      setEmailLoading(false);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedEmail(null);
  };

  const handleAskAI = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    try {
      setIsAskingAI(true);
      const response = await emailAPI.askQuestion(question);
      setAiAnswer(response.answer);
      setShowAIAnswer(true);
    } catch (error) {
      console.error('Error asking AI:', error);
      setAiAnswer('Sorry, I encountered an error while processing your question. Please try again.');
      setShowAIAnswer(true);
    } finally {
      setIsAskingAI(false);
    }
  };

  const clearAIAnswer = () => {
    setShowAIAnswer(false);
    setAiAnswer('');
    setQuestion('');
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays <= 7) {
      return date.toLocaleDateString([], { weekday: 'short' });
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
  };

  useEffect(() => {
    fetchEmails();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-rose-600 bg-clip-text text-transparent">Inbox Memory AI</h1>
            <button
              onClick={handleLogout}
              className="bg-rose-800 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition duration-200"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* AI Question Input */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <form onSubmit={handleAskAI} className="flex gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask AI about your emails..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent outline-none transition duration-200"
                disabled={isAskingAI}
              />
            </div>
            <button
              type="submit"
              disabled={isAskingAI || !question.trim()}
              className="bg-sky-600 text-white px-6 py-3 rounded-lg hover:bg-sky-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition duration-200 flex items-center gap-2"
            >
              {isAskingAI ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Asking...
                </>
              ) : (
                'Ask AI'
              )}
            </button>
            {showAIAnswer && (
              <button
                type="button"
                onClick={clearAIAnswer}
                className="bg-gray-500 text-white px-4 py-3 rounded-lg hover:bg-gray-600 transition duration-200"
              >
                Clear
              </button>
            )}
          </form>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-6">
        <div className={`flex gap-6 transition-all duration-500 ease-in-out ${showAIAnswer ? 'space-x-6' : ''}`}>
          {/* Email List */}
          <div className={`bg-white rounded-lg shadow overflow-hidden transition-all duration-500 ease-in-out ${
            showAIAnswer ? 'w-1/2' : 'w-full'
          }`}>
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Email KnowledgeBase 🧠</h2>
            </div>
            {loading ? (
              <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-sky-600"></div>
              </div>
            ) : emails.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-500">No emails found</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
                {emails.map((email) => (
                  <div
                    key={email.id}
                    onClick={() => handleEmailClick(email.id)}
                    className="px-6 py-4 hover:bg-gray-50 cursor-pointer transition duration-150 ease-in-out"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-3">
                          <div className="flex-shrink-0">
                            <div className="h-10 w-10 rounded-full bg-sky-500 flex items-center justify-center">
                              <span className="text-white font-medium text-sm">
                                {email.subject ? email.subject.charAt(0).toUpperCase() : 'E'}
                              </span>
                            </div>
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {email.subject || 'No Subject'}
                            </p>
                            <p className="text-sm text-gray-500">
                              Email content preview...
                            </p>
                          </div>
                        </div>
                      </div>
                      <div className="flex-shrink-0 text-sm text-gray-500">
                        {formatDate(email.created_at)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* AI Answer Panel */}
          {showAIAnswer && (
            <div className="w-1/2 bg-white rounded-lg shadow overflow-hidden transition-all duration-500 ease-in-out transform">
              <div className="px-6 py-4 border-b border-gray-200 bg-sky-50">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    <svg className="w-5 h-5 text-sky-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    AI Answer
                  </h2>
                  <button
                    onClick={clearAIAnswer}
                    className="text-gray-400 hover:text-gray-600 transition duration-200"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                <p className="text-sm text-gray-600 mt-1">"{question}"</p>
              </div>
              <div className="p-6 max-h-96 overflow-y-auto">
                <div className="prose prose-sm max-w-none">
                  <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{aiAnswer}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <EmailModal
        isOpen={isModalOpen}
        selectedEmail={selectedEmail}
        emailLoading={emailLoading}
        onClose={closeModal}
      />
    </div>
  );
};

export default Dashboard; 