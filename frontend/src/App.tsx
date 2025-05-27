import { useNavigate } from 'react-router';

function App() {
  const navigate = useNavigate();

  return (
    <div className='min-h-screen bg-gradient-to-br from-sky-50 via-white to-purple-50'>
      <div className='container mx-auto px-4 py-16'>
        <div className='text-center'>
          <h1 className='text-5xl font-bold text-gray-900 mb-6'>
            Welcome to{' '}
            <span className='bg-gradient-to-r from-purple-600 to-rose-600 bg-clip-text text-transparent'>
              InboxMemory AI
            </span>
          </h1>

          <p className='text-xl text-gray-600 mb-8 max-w-2xl mx-auto'>
            Your intelligent email memory assistant powered by RAG
            (Retrieval-Augmented Generation).
          </p>

          <div className='flex flex-col sm:flex-row gap-4 justify-center items-center'>
            <button
              onClick={() => navigate('/signup')}
              className='bg-sky-600 text-white px-8 py-3 rounded-lg hover:bg-sky-700 transition duration-200 font-medium text-lg'
            >
              New? Get Started
            </button>
            <button
              onClick={() => navigate('/login')}
              className='bg-white text-sky-600 px-8 py-3 rounded-lg border-2 border-sky-600 hover:bg-sky-50 transition duration-200 font-medium text-lg'
            >
              Sign In
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
