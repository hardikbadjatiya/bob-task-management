# Task Management System - Frontend

React TypeScript application with Vite for fast development and modern UI.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies**
```bash
npm install
```

2. **Configure environment**
```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
```

3. **Run development server**
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html           # HTML template
│
├── src/
│   ├── types/               # TypeScript type definitions
│   │   ├── user.ts
│   │   ├── task.ts
│   │   └── api.ts
│   │
│   ├── services/            # API service layer
│   │   ├── api.ts           # Axios configuration
│   │   ├── authService.ts   # Authentication API
│   │   └── taskService.ts   # Task management API
│   │
│   ├── components/          # React components (future)
│   │   ├── Auth/
│   │   ├── Tasks/
│   │   └── Common/
│   │
│   ├── hooks/               # Custom React hooks (future)
│   ├── utils/               # Utility functions (future)
│   │
│   ├── App.tsx              # Main app component
│   ├── App.css              # App styles
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles
│
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite configuration
└── README.md
```

## 🛠️ Available Scripts

### Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Code Quality
```bash
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
```

### Testing
```bash
npm run test         # Run tests
npm run test:ui      # Run tests with UI
npm run test:coverage # Generate coverage report
```

## 🔑 Features

- **Authentication**: JWT-based login/register
- **Task Management**: Create, read, update, delete tasks
- **Filtering**: Filter tasks by status, priority, assignee
- **Responsive Design**: Works on desktop and mobile
- **Type Safety**: Full TypeScript support
- **Modern UI**: Clean and intuitive interface

## 🎨 Tech Stack

- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **Zustand**: State management (ready to use)
- **CSS3**: Styling

## 📡 API Integration

The frontend communicates with the FastAPI backend:

- Base URL: `http://localhost:8000`
- API Prefix: `/api/v1`
- Authentication: JWT Bearer tokens

### API Endpoints Used

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/tasks/` - List tasks
- `POST /api/v1/tasks/` - Create task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

## 🔒 Authentication Flow

1. User logs in with email/password
2. Backend returns access_token and refresh_token
3. Tokens stored in localStorage
4. Access token sent with each API request
5. Automatic token refresh on 401 errors

## 🎯 Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## 📦 Building for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

## 🚀 Deployment

### Static Hosting (Netlify, Vercel, etc.)

1. Build the project: `npm run build`
2. Deploy the `dist/` folder
3. Configure environment variables on the platform

### Docker

```bash
docker build -t task-frontend .
docker run -p 3000:80 task-frontend
```

## 🧪 Testing

Tests are configured with Vitest and React Testing Library:

```bash
npm run test
```

## 🎨 Styling

- CSS Modules for component styles
- Global styles in `index.css`
- Responsive design with flexbox and grid
- Modern gradient backgrounds

## 🔧 Development Tips

1. **Hot Module Replacement**: Changes reflect instantly
2. **TypeScript**: Catch errors before runtime
3. **ESLint**: Maintain code quality
4. **Prettier**: Consistent code formatting

## 📝 Future Enhancements

- [ ] React Router for multi-page navigation
- [ ] Advanced task filtering and search
- [ ] Real-time updates with WebSockets
- [ ] Drag-and-drop task management
- [ ] Dark mode support
- [ ] Internationalization (i18n)
- [ ] Progressive Web App (PWA)

## 🤝 Contributing

1. Follow TypeScript best practices
2. Write tests for new features
3. Use ESLint and Prettier
4. Update documentation

## 📄 License

MIT License