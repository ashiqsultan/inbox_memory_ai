

interface EmailContent {
  id: string;
  user_id: string;
  subject: string;
  content_html: string;
  content_text: string;
  created_at: string;
}

interface EmailModalProps {
  isOpen: boolean;
  selectedEmail: EmailContent | null;
  emailLoading: boolean;
  onClose: () => void;
}

const EmailModal = ({ isOpen, selectedEmail, emailLoading, onClose }: EmailModalProps) => {
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

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 flex items-center justify-center z-50 p-4"
      style={{
        backgroundColor: 'rgba(0, 0, 0, 0.3)',
        backdropFilter: 'blur(4px)',
        WebkitBackdropFilter: 'blur(4px)'
      }}
    >
      <div className="w-4/5 h-4/5 max-w-6xl max-h-screen border shadow-lg rounded-md bg-white overflow-hidden flex flex-col">
        {/* Modal Header */}
        <div className="flex justify-between items-start p-6 border-b border-gray-200 flex-shrink-0">
          <div className="flex-1">
            <h3 className="text-lg font-medium text-gray-900">
              {selectedEmail?.subject || 'No Subject'}
            </h3>
            <p className="text-sm text-gray-500 mt-1">
              {selectedEmail?.created_at && formatDate(selectedEmail.created_at)}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition duration-150 ease-in-out"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Modal Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {emailLoading ? (
            <div className="flex justify-center items-center h-full">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : selectedEmail ? (
            <div>
              {selectedEmail.content_html ? (
                <div 
                  className="prose max-w-none"
                  dangerouslySetInnerHTML={{ __html: selectedEmail.content_html }}
                />
              ) : (
                <div className="whitespace-pre-wrap text-gray-700">
                  {selectedEmail.content_text || 'No content available'}
                </div>
              )}
            </div>
          ) : null}
        </div>

        {/* Modal Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200 flex-shrink-0">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition duration-200"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default EmailModal; 