import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  LinearProgress,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Recycling as RecyclingIcon,
  Park as EcoIcon,
  LocalShipping as ShippingIcon,
} from '@mui/icons-material';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

interface WasteRecord {
  id: string;
  type: string;
  amount: number;
  unit: string;
  disposal: string;
  recyclingRate: number;
  date: string;
  location: string;
}

const CircularEconomy: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState<WasteRecord | null>(null);
  const [formData, setFormData] = useState({
    type: '',
    amount: '',
    unit: 'kg',
    disposal: '',
    recyclingRate: '',
    location: '',
  });

  const [records, setRecords] = useState<WasteRecord[]>([
    {
      id: '1',
      type: '종이',
      amount: 2500,
      unit: 'kg',
      disposal: '재활용',
      recyclingRate: 95,
      date: '2024-01-15',
      location: '본사',
    },
    {
      id: '2',
      type: '플라스틱',
      amount: 800,
      unit: 'kg',
      disposal: '재활용',
      recyclingRate: 85,
      date: '2024-01-14',
      location: '본사',
    },
    {
      id: '3',
      type: '전자폐기물',
      amount: 120,
      unit: 'kg',
      disposal: '재활용',
      recyclingRate: 90,
      date: '2024-01-13',
      location: '본사',
    },
    {
      id: '4',
      type: '음식물 쓰레기',
      amount: 600,
      unit: 'kg',
      disposal: '퇴비화',
      recyclingRate: 100,
      date: '2024-01-12',
      location: '본사',
    },
  ]);

  const wasteTypes = [
    '종이',
    '플라스틱',
    '전자폐기물',
    '음식물 쓰레기',
    '유리',
    '금속',
    '기타',
  ];

  const disposalMethods = [
    '재활용',
    '퇴비화',
    '에너지 회수',
    '매립',
  ];

  const wasteData = [
    { name: '재활용', value: 3420, color: '#82ca9d' },
    { name: '퇴비화', value: 600, color: '#8884d8' },
    { name: '에너지 회수', value: 200, color: '#ffc658' },
    { name: '매립', value: 0, color: '#ff7300' },
  ];

  const monthlyData = [
    { name: '1월', recycled: 3200, composted: 550, energy: 180, landfill: 0 },
    { name: '2월', recycled: 3100, composted: 520, energy: 170, landfill: 0 },
    { name: '3월', recycled: 3300, composted: 580, energy: 190, landfill: 0 },
    { name: '4월', recycled: 3400, composted: 600, energy: 200, landfill: 0 },
    { name: '5월', recycled: 3500, composted: 620, energy: 210, landfill: 0 },
    { name: '6월', recycled: 3600, composted: 650, energy: 220, landfill: 0 },
  ];

  const handleOpen = () => {
    setFormData({
      type: '',
      amount: '',
      unit: 'kg',
      disposal: '',
      recyclingRate: '',
      location: '',
    });
    setEditingRecord(null);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingRecord(null);
  };

  const handleSubmit = () => {
    if (editingRecord) {
      setRecords(records.map(record => 
        record.id === editingRecord.id 
          ? { ...record, ...formData, amount: parseFloat(formData.amount), recyclingRate: parseFloat(formData.recyclingRate) }
          : record
      ));
    } else {
      const newRecord: WasteRecord = {
        id: Date.now().toString(),
        ...formData,
        amount: parseFloat(formData.amount),
        recyclingRate: parseFloat(formData.recyclingRate),
        date: new Date().toISOString().split('T')[0],
      };
      setRecords([...records, newRecord]);
    }
    handleClose();
  };

  const handleEdit = (record: WasteRecord) => {
    setFormData({
      type: record.type,
      amount: record.amount.toString(),
      unit: record.unit,
      disposal: record.disposal,
      recyclingRate: record.recyclingRate.toString(),
      location: record.location,
    });
    setEditingRecord(record);
    setOpen(true);
  };

  const handleDelete = (id: string) => {
    setRecords(records.filter(record => record.id !== id));
  };

  const totalWaste = records.reduce((sum, record) => sum + record.amount, 0);
  const recycledWaste = records.filter(r => r.disposal === '재활용').reduce((sum, record) => sum + record.amount, 0);
  const overallRecyclingRate = (recycledWaste / totalWaste) * 100;
  const landfillWaste = records.filter(r => r.disposal === '매립').reduce((sum, record) => sum + record.amount, 0);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          순환경제 관리
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleOpen}
        >
          폐기물 등록
        </Button>
      </Box>

      {/* 매립 제로화 알림 */}
      {landfillWaste === 0 && (
        <Alert severity="success" sx={{ mb: 3 }}>
          🎉 매립 제로화 달성! 모든 폐기물이 재활용되거나 친환경적으로 처리되고 있습니다.
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* 요약 카드 */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <RecyclingIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">총 폐기물</Typography>
              </Box>
              <Typography variant="h4" color="primary">
                {totalWaste.toLocaleString()}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                kg
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <EcoIcon sx={{ mr: 1, color: 'success.main' }} />
                <Typography variant="h6">재활용률</Typography>
              </Box>
              <Typography variant="h4" color="success.main">
                {overallRecyclingRate.toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                달성률
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>매립 제로화</Typography>
              <Typography variant="h4" color={landfillWaste === 0 ? 'success.main' : 'warning.main'}>
                {landfillWaste === 0 ? '100%' : '95%'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                달성률
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>자원 회수</Typography>
              <Typography variant="h4" color="info.main">
                92%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                회수율
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* 폐기물 처리 방법별 비율 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="폐기물 처리 방법별 비율" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={wasteData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {wasteData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* 월별 폐기물 처리 현황 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="월별 폐기물 처리 현황" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="recycled" stackId="a" fill="#82ca9d" name="재활용" />
                  <Bar dataKey="composted" stackId="a" fill="#8884d8" name="퇴비화" />
                  <Bar dataKey="energy" stackId="a" fill="#ffc658" name="에너지 회수" />
                  <Bar dataKey="landfill" stackId="a" fill="#ff7300" name="매립" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* 순환경제 지표 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="순환경제 지표" />
            <CardContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="subtitle1">재활용률</Typography>
                      <Typography variant="body2">85% / 90%</Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={(85 / 90) * 100} 
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="subtitle1">매립 제로화</Typography>
                      <Typography variant="body2">100% / 100%</Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={100} 
                      sx={{ height: 8, borderRadius: 4 }}
                      color="success"
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="subtitle1">자원 회수</Typography>
                      <Typography variant="body2">92% / 95%</Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={(92 / 95) * 100} 
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* 순환경제 프로젝트 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="순환경제 프로젝트" />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                    <Typography variant="h6" gutterBottom>스마트 폐기물 관리</Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      IoT 센서를 활용한 폐기물 분리수거 시스템 구축
                    </Typography>
                    <Chip label="완료" color="success" size="small" sx={{ mt: 1 }} />
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                    <Typography variant="h6" gutterBottom>업사이클링 센터</Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      폐기물을 새로운 제품으로 재생산하는 센터 운영
                    </Typography>
                    <Chip label="진행중" color="warning" size="small" sx={{ mt: 1 }} />
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                    <Typography variant="h6" gutterBottom>디지털 패스포트</Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      제품의 생애주기 추적을 위한 디지털 패스포트 시스템
                    </Typography>
                    <Chip label="계획" color="info" size="small" sx={{ mt: 1 }} />
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* 폐기물 기록 테이블 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="폐기물 처리 기록" />
            <CardContent>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>폐기물 유형</TableCell>
                      <TableCell>양</TableCell>
                      <TableCell>처리 방법</TableCell>
                      <TableCell>재활용률</TableCell>
                      <TableCell>위치</TableCell>
                      <TableCell>날짜</TableCell>
                      <TableCell>액션</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {records.map((record) => (
                      <TableRow key={record.id}>
                        <TableCell>{record.type}</TableCell>
                        <TableCell>{record.amount.toLocaleString()} {record.unit}</TableCell>
                        <TableCell>
                          <Chip 
                            label={record.disposal} 
                            color={record.disposal === '재활용' ? 'success' : record.disposal === '퇴비화' ? 'info' : 'default'}
                            size="small" 
                          />
                        </TableCell>
                        <TableCell>{record.recyclingRate}%</TableCell>
                        <TableCell>{record.location}</TableCell>
                        <TableCell>{record.date}</TableCell>
                        <TableCell>
                          <IconButton onClick={() => handleEdit(record)}>
                            <EditIcon />
                          </IconButton>
                          <IconButton onClick={() => handleDelete(record.id)}>
                            <DeleteIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 폐기물 등록/수정 다이얼로그 */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingRecord ? '폐기물 수정' : '폐기물 등록'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <FormControl fullWidth margin="normal">
              <InputLabel>폐기물 유형</InputLabel>
              <Select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              >
                {wasteTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="양"
              type="number"
              value={formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>처리 방법</InputLabel>
              <Select
                value={formData.disposal}
                onChange={(e) => setFormData({ ...formData, disposal: e.target.value })}
              >
                {disposalMethods.map((method) => (
                  <MenuItem key={method} value={method}>
                    {method}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="재활용률 (%)"
              type="number"
              value={formData.recyclingRate}
              onChange={(e) => setFormData({ ...formData, recyclingRate: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="위치"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              margin="normal"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>취소</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingRecord ? '수정' : '등록'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CircularEconomy;

