import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router';
import { authAPI } from '../../services/api';

const VerifyOTP = () => {
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  const email = location.state?.email;

  useEffect(() => {
    if (!email) {
      navigate('/login');
    }
  }, [email, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const data = await authAPI.verifyOTP(email, otp);

      if (data.verified) {
        setMessage('OTP verified successfully!');
        // Store the access token
        localStorage.setItem('access_token', data.access_token);
        // Navigate to dashboard or home page
        setTimeout(() => {
          navigate('/dashboard');
        }, 1500);
      } else {
        setMessage(data.message || 'Invalid or expired OTP');
      }
    } catch (error: any) {
      setMessage(
        error.response?.data?.message || 'Network error. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  if (!email) {
    return null;
  }

  return (
    <div className='min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100'>
      <div className='max-w-md w-full space-y-8 p-8'>
        <div className='bg-white rounded-2xl shadow-xl p-8'>
          <div className='text-center'>
            <div className='mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4'>
              <svg
                className='w-8 h-8 text-green-600'
                fill='none'
                stroke='currentColor'
                viewBox='0 0 24 24'
              >
                <path
                  strokeLinecap='round'
                  strokeLinejoin='round'
                  strokeWidth={2}
                  d='M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'
                />
              </svg>
            </div>
            <h2 className='text-3xl font-bold text-gray-900 mb-2'>
              Verify Your Email
            </h2>
            <p className='text-gray-600 mb-2'>
              We've sent a verification code to
            </p>
            <p className='text-green-600 font-medium mb-8'>{email}</p>
          </div>

          <form onSubmit={handleSubmit} className='space-y-6'>
            <div>
              <label
                htmlFor='otp'
                className='block text-sm font-medium text-gray-700 mb-2'
              >
                Verification Code
              </label>
              <input
                id='otp'
                type='text'
                value={otp}
                onChange={(e) =>
                  setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))
                }
                required
                maxLength={6}
                className='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200 ease-in-out text-center text-2xl font-mono tracking-widest'
                placeholder='000000'
              />
              <p className='text-xs text-gray-500 mt-1'>
                Enter the 6-digit code from your email
              </p>
            </div>

            <button
              type='submit'
              disabled={loading || otp.length !== 6}
              className='w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-200 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed font-medium'
            >
              {loading ? 'Verifying...' : 'Verify Code'}
            </button>
          </form>

          {message && (
            <div
              className={`mt-4 p-3 rounded-lg text-sm ${
                message.includes('successfully') || message.includes('sent')
                  ? 'bg-green-50 text-green-700 border border-green-200'
                  : 'bg-red-50 text-red-700 border border-red-200'
              }`}
            >
              {message}
            </div>
          )}

          <div className='mt-4 text-center'>
            <button
              onClick={() => navigate('/login')}
              className='text-gray-500 hover:text-gray-700 text-sm'
            >
              ← Back to Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifyOTP;
