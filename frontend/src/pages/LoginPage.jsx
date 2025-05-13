import React from 'react';
import Layout from '../components/layout/Layout';
import LoginForm from '../components/auth/LoginForm';

function LoginPage() {
  return (
    <Layout>
      <div className="auth-page">
        <div className="container">
          <div className="auth-page__content">
            <LoginForm />
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default LoginPage; 