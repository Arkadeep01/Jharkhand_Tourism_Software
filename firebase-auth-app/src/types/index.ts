export interface User {
  uid: string;
  email: string;
  displayName?: string;
  photoURL?: string;
}

export interface AuthFormProps {
  onSubmit: (email: string, password: string) => void;
  isSignUp?: boolean;
}