import { MOCK_USERS } from '../data/mockUsers';

export function authenticateUser(email, password, role) {
  const normalizedEmail = email.trim().toLowerCase();
  
  const foundUser = MOCK_USERS.find(user => 
    user.email.toLowerCase() === normalizedEmail &&
    user.password === password
  );

  if (foundUser) {
    // Return sanitized session user object
    const { password: _, ...userSession } = foundUser;
    return { success: true, user: userSession };
  }

  return { 
    success: false, 
    error: "Invalid email or password. Please check your credentials." 
  };
}

