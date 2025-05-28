import { useNavigate } from 'react-router';
import {
  Mail,
  Search,
  Brain,
  ArrowRight,
  Github,
  Linkedin,
  Zap,
} from 'lucide-react';

function App() {
  const navigate = useNavigate();

  return (
    <div className='h-screen w-full bg-gradient-to-br from-purple-50 via-sky-50 to-rose-50 overflow-hidden'>
      {/* Navigation */}
      <nav className='absolute top-0 left-0 right-0 z-10 p-6'>
        <div className='flex justify-between items-center'>
          <div className='flex items-center space-x-2'>
            <Brain className='h-8 w-8 text-purple-600' />
            <span className='text-2xl font-bold bg-gradient-to-r from-purple-600 to-rose-600 bg-clip-text text-transparent'>
              InboxMemory AI
            </span>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className='h-full flex items-center justify-center px-6'>
        <div className='max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-center'>
          {/* Left Side - Content */}
          <div className='space-y-8'>
            <div className='space-y-6'>
              <h1 className='text-6xl lg:text-7xl font-bold leading-tight'>
                <span className='text-gray-900'>Your Email</span>
                <br />
                <span className='bg-gradient-to-r from-purple-600 via-sky-600 to-rose-600 bg-clip-text text-transparent'>
                  Memory Assistant
                </span>
              </h1>

              <p className='text-xl text-gray-600 leading-relaxed max-w-lg'>
                Forward any email → AI stores it as searchable knowledge → Ask
                questions later and get instant answers.
                <span className='font-semibold text-gray-800'>
                  {' '}
                  No organizing, no folders, just email and ask.
                </span>
              </p>
            </div>

            {/* Features */}
            <div className='space-y-4'>
              <div className='flex items-center space-x-3 text-gray-700'>
                <div className='p-2 bg-purple-100 rounded-lg'>
                  <Mail className='h-5 w-5 text-purple-600' />
                </div>
                <span>Forward anything interesting to your AI assistant</span>
              </div>
              <div className='flex items-center space-x-3 text-gray-700'>
                <div className='p-2 bg-sky-100 rounded-lg'>
                  <Search className='h-5 w-5 text-sky-600' />
                </div>
                <span>
                  Ask questions like "What was that restaurant from Sarah?"
                </span>
              </div>
              <div className='flex items-center space-x-3 text-gray-700'>
                <div className='p-2 bg-rose-100 rounded-lg'>
                  <Zap className='h-5 w-5 text-rose-600' />
                </div>
                <span>Get instant answers from your email knowledge base</span>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className='flex flex-col sm:flex-row gap-4 pt-4'>
              <button
                onClick={() => navigate('/signup')}
                className='group bg-purple-600  text-white px-8 py-4 rounded-xl hover:bg-purple-500 transition-all duration-200 font-semibold text-lg flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl'
              >
                <span>Get Started Free</span>
                <ArrowRight className='h-5 w-5 group-hover:translate-x-1 transition-transform' />
              </button>
              <div className='flex gap-4'>
                <button
                  onClick={() => navigate('/login')}
                  className='bg-white/80 backdrop-blur-sm text-gray-800 px-8 py-4 rounded-xl border-2 border-gray-200 hover:bg-white hover:border-purple-300 transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl'
                >
                  Sign In
                </button>
                <a
                  href='https://github.com/ashiqsultan/inbox_memory_ai'
                  target='_blank'
                  rel='noopener noreferrer'
                  className='bg-gray-900 hover:bg-gray-800 text-white px-4 py-4 rounded-xl transition-all duration-200 flex items-center justify-center shadow-lg hover:shadow-xl'
                >
                  <Github className='h-6 w-6' />
                </a>
                <a
                  href='https://www.linkedin.com/in/ashiq-sultan/'
                  target='_blank'
                  rel='noopener noreferrer'
                  className='bg-blue-600 hover:bg-blue-700 text-white px-4 py-4 rounded-xl transition-all duration-200 flex items-center justify-center shadow-lg hover:shadow-xl'
                >
                  <Linkedin className='h-6 w-6' />
                </a>
              </div>
            </div>
          </div>

          {/* Right Side - Visual */}
          <div className='relative'>
            <div className='relative z-10 bg-white/90 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border border-gray-200'>
              <div className='space-y-6'>
                <div className='flex items-center space-x-3 pb-4 border-b border-gray-100'>
                  <div className='p-2 bg-sky-600 rounded-lg'>
                    <Mail className='h-6 w-6 text-white' />
                  </div>
                  <div>
                    <h3 className='font-semibold text-gray-900'>
                      Example Query
                    </h3>
                    <p className='text-sm text-gray-500'>
                      Try asking your AI assistant
                    </p>
                  </div>
                </div>

                <div className='space-y-4'>
                  <div className='bg-gray-50 rounded-lg p-4'>
                    <p className='text-gray-700 italic'>
                      "What was that vacation rental link John sent me last
                      month?"
                    </p>
                  </div>

                  <div className='bg-gradient-to-r from-purple-50 to-rose-50 rounded-lg p-4 border-l-4 border-purple-400'>
                    <p className='text-gray-800 font-medium'>
                      Found it! John sent you an Airbnb link for a cabin in
                      Aspen on March 15th. The property was $280/night and had a
                      hot tub.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Background decorative elements */}
            <div className='absolute -top-4 -right-4 w-72 h-72 bg-gradient-to-br from-purple-200 to-rose-200 rounded-full opacity-20 blur-3xl'></div>
            <div className='absolute -bottom-8 -left-8 w-64 h-64 bg-gradient-to-br from-sky-200 to-purple-200 rounded-full opacity-20 blur-3xl'></div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
