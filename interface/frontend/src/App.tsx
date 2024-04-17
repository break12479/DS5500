import { PageContainer, ProCard, ProLayout } from '@ant-design/pro-components';
import { useState } from 'react';
import Dashboard from './pages/dashboard';

const defaultProps = {
  route: {
    path: '/',
    routes: [
      {
        path: '/dashboard',
        name: '总结',
        component: <Dashboard/>,
      },
    ],
  },
};

const App = () => {
  const [pathname, setPathname] = useState('/dashboard');
  const [component, setComponent] = useState(<Dashboard/>);
  
  return (
    <div
      id="test-pro-layout"
      style={{
        height: '100vh',
      }}
    >


        <PageContainer>
          <ProCard
            style={{
              height: '100vh',
              minHeight: 800,
            }}
          >
            {component}
          </ProCard>
        </PageContainer>

    </div>
  );
};

export default App;