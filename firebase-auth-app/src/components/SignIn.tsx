import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';
import AuthForm from '../components/AuthForm';

const SignIn: React.FC = () => {
  const [error, setError] = useState('');

  const handleSubmit = async (email: string, password: string) => {
    setError('');
    try {
      await signInWithEmailAndPassword(auth, email, password);
      console.log("✅ Sign in successful");
      // TODO: redirect user (e.g., navigate to home page)
    } catch (err) {
      console.error(err);
      setError('Failed to sign in. Please check your credentials.');
    }
  };

  return (
    <div>
      <AuthForm onSubmit={handleSubmit} errorMessage={error} isSignUp={false} />
    </div>
  );
};

export default SignIn;
