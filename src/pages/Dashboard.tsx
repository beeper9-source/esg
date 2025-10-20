import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardHeader,
  LinearProgress,
  Chip,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

const Dashboard: React.FC = () => {
  // 샘플 데이터
  const emissionData = [
    { name: '1월', scope1: 1200, scope2: 800, scope3: 2000 },
    { name: '2월', scope1: 1100, scope2: 750, scope3: 1900 },
    { name: '3월', scope1: 1000, scope2: 700, scope3: 1800 },
    { name: '4월', scope1: 950, scope2: 680, scope3: 1750 },
    { name: '5월', scope1: 900, scope2: 650, scope3: 1700 },
    { name: '6월', scope1: 850, scope2: 620, scope3: 1650 },
  ];

  const scopeData = [
    { name: 'Scope 1', value: 850, color: '#8884d8' },
    { name: 'Scope 2', value: 620, color: '#82ca9d' },
    { name: 'Scope 3', value: 1650, color: '#ffc658' },
  ];

  const circularEconomyData = [
    { name: '재활용률', value: 85, target: 90 },
    { name: '매립 제로화', value: 95, target: 100 },
    { name: '에너지 효율', value: 78, target: 85 },
  ];

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3 }}>
        탄소관리 대시보드
      </Typography>

      <Grid container spacing={3}>
        {/* 전체 배출량 현황 */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardHeader title="월별 온실가스 배출량 추이" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={emissionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="scope1" stroke="#8884d8" strokeWidth={2} />
                  <Line type="monotone" dataKey="scope2" stroke="#82ca9d" strokeWidth={2} />
                  <Line type="monotone" dataKey="scope3" stroke="#ffc658" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Scope별 배출량 비율 */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Scope별 배출량 비율" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={scopeData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {scopeData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* 순환경제 지표 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="순환경제 달성률" />
            <CardContent>
              <Grid container spacing={3}>
                {circularEconomyData.map((item) => (
                  <Grid item xs={12} md={4} key={item.name}>
                    <Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="subtitle1">{item.name}</Typography>
                        <Chip 
                          label={`${item.value}%`} 
                          color={item.value >= item.target ? 'success' : 'warning'}
                          size="small"
                        />
                      </Box>
                      <LinearProgress 
                        variant="determinate" 
                        value={(item.value / item.target) * 100} 
                        sx={{ height: 8, borderRadius: 4 }}
                      />
                      <Typography variant="caption" color="text.secondary">
                        목표: {item.target}%
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* 주요 성과 지표 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="주요 성과 지표" />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="primary">-15%</Typography>
                    <Typography variant="subtitle2">전년 대비 배출량 감소</Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="success.main">85%</Typography>
                    <Typography variant="subtitle2">재활용률</Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="info.main">95%</Typography>
                    <Typography variant="subtitle2">매립 제로화</Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="warning.main">127</Typography>
                    <Typography variant="subtitle2">제안된 아이디어</Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* 최근 활동 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="최근 활동" />
            <CardContent>
              <Box>
                <Typography variant="body2" gutterBottom>
                  • 사무용 전기차 충전소 설치 완료 (Scope 1 감소)
                </Typography>
                <Typography variant="body2" gutterBottom>
                  • 재생에너지 구매 계약 체결 (Scope 2 감소)
                </Typography>
                <Typography variant="body2" gutterBottom>
                  • 공급업체 탄소중립 협약 체결 (Scope 3 감소)
                </Typography>
                <Typography variant="body2" gutterBottom>
                  • 폐기물 재활용 시스템 개선 (순환경제)
                </Typography>
                <Typography variant="body2">
                  • 임직원 아이디어 15건 접수
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;

