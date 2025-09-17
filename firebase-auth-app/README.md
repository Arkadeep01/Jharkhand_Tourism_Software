# React Firebase Auth App

This project is a simple React application that provides sign-in and sign-up functionality using Firebase for authentication. It is structured to separate components, pages, and Firebase configuration for better maintainability.

## Project Structure

```
react-firebase-auth-app
├── src
│   ├── components
│   │   ├── SignIn.tsx        # Sign-in form component
│   │   ├── SignUp.tsx       # Sign-up form component
│   │   └── AuthForm.tsx     # Reusable authentication form component
│   ├── firebase
│   │   └── config.ts        # Firebase configuration and initialization
│   ├── pages
│   │   ├── SignInPage.tsx   # Page component for sign-in
│   │   └── SignUpPage.tsx   # Page component for sign-up
│   ├── App.tsx              # Main application component with routing
│   ├── index.tsx            # Entry point of the application
│   └── types
│       └── index.ts         # TypeScript interfaces and types
├── public
│   └── index.html           # Main HTML file
├── package.json             # NPM configuration file
├── tsconfig.json            # TypeScript configuration file
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd react-firebase-auth-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Firebase Configuration:**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/).
   - Add your web app to the project and copy the Firebase configuration.
   - Update the `src/firebase/config.ts` file with your Firebase configuration.

4. **Run the application:**
   ```bash
   npm start
   ```

5. **Access the application:**
   Open your browser and navigate to `http://localhost:3000`.

## Usage

- Navigate to the sign-in page to log in with existing credentials.
- Navigate to the sign-up page to create a new account.
- The application uses Firebase for authentication, ensuring secure user management.

## License

This project is licensed under the MIT License.