import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Factory as FactoryIcon,
  ElectricalServices as ElectricalIcon,
  Business as BusinessIcon,
  Recycling as RecyclingIcon,
  Lightbulb as LightbulbIcon,
  Park as EcoIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: '대시보드', icon: <DashboardIcon />, path: '/' },
  { text: 'Scope 1 (직접 배출)', icon: <FactoryIcon />, path: '/scope1' },
  { text: 'Scope 2 (간접 배출)', icon: <ElectricalIcon />, path: '/scope2' },
  { text: 'Scope 3 (밸류체인)', icon: <BusinessIcon />, path: '/scope3' },
  { text: '순환경제', icon: <RecyclingIcon />, path: '/circular-economy' },
  { text: '임직원 아이디어', icon: <LightbulbIcon />, path: '/ideas' },
];

const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          backgroundColor: '#1e3a8a',
          color: 'white',
        },
      }}
    >
      <Box 
        sx={{ 
          p: 2, 
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: 1,
          '&:hover': {
            backgroundColor: 'rgba(255,255,255,0.05)',
          },
          transition: 'background-color 0.2s',
        }}
        onClick={() => navigate('/')}
      >
        <EcoIcon sx={{ fontSize: 28, color: '#4ade80' }} />
        <Box>
          <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
            삼성SDS ESG
          </Typography>
          <Typography variant="subtitle2" sx={{ opacity: 0.8 }}>
            탄소관리 시스템
          </Typography>
        </Box>
      </Box>
      <Divider sx={{ backgroundColor: 'rgba(255,255,255,0.2)' }} />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              onClick={() => navigate(item.path)}
              selected={location.pathname === item.path}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: 'rgba(255,255,255,0.1)',
                  '&:hover': {
                    backgroundColor: 'rgba(255,255,255,0.15)',
                  },
                },
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.05)',
                },
              }}
            >
              <ListItemIcon sx={{ color: 'white' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Navigation;

