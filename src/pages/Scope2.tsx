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
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  ElectricalServices as ElectricalIcon,
  SolarPower as SolarIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface EnergyRecord {
  id: string;
  type: string;
  source: string;
  amount: number;
  unit: string;
  date: string;
  location: string;
  renewable: boolean;
}

const Scope2: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState<EnergyRecord | null>(null);
  const [formData, setFormData] = useState({
    type: '',
    source: '',
    amount: '',
    unit: 'kWh',
    location: '',
    renewable: false,
  });

  const [records, setRecords] = useState<EnergyRecord[]>([
    {
      id: '1',
      type: '전력',
      source: '한국전력공사',
      amount: 15000,
      unit: 'kWh',
      date: '2024-01-15',
      location: '본사',
      renewable: false,
    },
    {
      id: '2',
      type: '전력',
      source: '재생에너지',
      amount: 5000,
      unit: 'kWh',
      date: '2024-01-15',
      location: '본사',
      renewable: true,
    },
    {
      id: '3',
      type: '냉난방',
      source: '지역난방공사',
      amount: 2500,
      unit: 'GJ',
      date: '2024-01-14',
      location: '본사',
      renewable: false,
    },
  ]);

  const energyTypes = [
    '전력',
    '냉난방',
    '증기',
    '기타 에너지',
  ];

  const monthlyData = [
    { name: '1월', total: 22000, renewable: 5000, conventional: 17000 },
    { name: '2월', total: 21000, renewable: 4800, conventional: 16200 },
    { name: '3월', total: 20000, renewable: 5200, conventional: 14800 },
    { name: '4월', total: 19500, renewable: 5500, conventional: 14000 },
    { name: '5월', total: 19000, renewable: 6000, conventional: 13000 },
    { name: '6월', total: 18500, renewable: 6500, conventional: 12000 },
  ];

  const energySourceData = [
    { name: '재생에너지', value: 6500, color: '#82ca9d' },
    { name: '일반전력', value: 12000, color: '#8884d8' },
  ];

  const handleOpen = () => {
    setFormData({
      type: '',
      source: '',
      amount: '',
      unit: 'kWh',
      location: '',
      renewable: false,
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
          ? { ...record, ...formData, amount: parseFloat(formData.amount) }
          : record
      ));
    } else {
      const newRecord: EnergyRecord = {
        id: Date.now().toString(),
        ...formData,
        amount: parseFloat(formData.amount),
        date: new Date().toISOString().split('T')[0],
      };
      setRecords([...records, newRecord]);
    }
    handleClose();
  };

  const handleEdit = (record: EnergyRecord) => {
    setFormData({
      type: record.type,
      source: record.source,
      amount: record.amount.toString(),
      unit: record.unit,
      location: record.location,
      renewable: record.renewable,
    });
    setEditingRecord(record);
    setOpen(true);
  };

  const handleDelete = (id: string) => {
    setRecords(records.filter(record => record.id !== id));
  };

  const totalEnergy = records.reduce((sum, record) => sum + record.amount, 0);
  const renewableEnergy = records.filter(r => r.renewable).reduce((sum, record) => sum + record.amount, 0);
  const renewableRatio = (renewableEnergy / totalEnergy) * 100;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Scope 2 - 간접 배출량 관리
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleOpen}
        >
          에너지 사용량 등록
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* 요약 카드 */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <ElectricalIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">총 에너지 사용량</Typography>
              </Box>
              <Typography variant="h4" color="primary">
                {totalEnergy.toLocaleString()}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                kWh
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SolarIcon sx={{ mr: 1, color: 'success.main' }} />
                <Typography variant="h6">재생에너지 비율</Typography>
              </Box>
              <Typography variant="h4" color="success.main">
                {renewableRatio.toFixed(1)}%
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
              <Typography variant="h6" gutterBottom>전년 대비</Typography>
              <Typography variant="h4" color="success.main">
                -8%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                에너지 절약
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>목표 달성률</Typography>
              <Typography variant="h4" color="info.main">
                92%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                달성
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* 월별 에너지 사용량 추이 */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardHeader title="월별 에너지 사용량 추이" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="total" stroke="#8884d8" strokeWidth={2} name="총 사용량" />
                  <Line type="monotone" dataKey="renewable" stroke="#82ca9d" strokeWidth={2} name="재생에너지" />
                  <Line type="monotone" dataKey="conventional" stroke="#ffc658" strokeWidth={2} name="일반에너지" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* 에너지원별 비율 */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="에너지원별 비율" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={energySourceData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {energySourceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* 에너지 효율 개선 활동 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="에너지 효율 개선 활동" />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                    <Typography variant="h6" gutterBottom>LED 조명 전환</Typography>
                    <Typography variant="body2" color="text.secondary">
                      기존 형광등을 LED로 전환하여 전력 사용량 30% 절약
                    </Typography>
                    <Chip label="완료" color="success" size="small" sx={{ mt: 1 }} />
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                    <Typography variant="h6" gutterBottom>스마트 빌딩 시스템</Typography>
                    <Typography variant="body2" color="text.secondary">
                      IoT 센서를 활용한 자동 에너지 관리 시스템 구축
                    </Typography>
                    <Chip label="진행중" color="warning" size="small" sx={{ mt: 1 }} />
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                    <Typography variant="h6" gutterBottom>재생에너지 확대</Typography>
                    <Typography variant="body2" color="text.secondary">
                      태양광 발전소 추가 설치로 재생에너지 비율 확대
                    </Typography>
                    <Chip label="계획" color="info" size="small" sx={{ mt: 1 }} />
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* 에너지 사용량 기록 테이블 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="에너지 사용량 기록" />
            <CardContent>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>에너지 유형</TableCell>
                      <TableCell>공급원</TableCell>
                      <TableCell>사용량</TableCell>
                      <TableCell>위치</TableCell>
                      <TableCell>재생에너지</TableCell>
                      <TableCell>날짜</TableCell>
                      <TableCell>액션</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {records.map((record) => (
                      <TableRow key={record.id}>
                        <TableCell>{record.type}</TableCell>
                        <TableCell>{record.source}</TableCell>
                        <TableCell>{record.amount.toLocaleString()} {record.unit}</TableCell>
                        <TableCell>{record.location}</TableCell>
                        <TableCell>
                          <Chip 
                            label={record.renewable ? '재생에너지' : '일반에너지'} 
                            color={record.renewable ? 'success' : 'default'}
                            size="small" 
                          />
                        </TableCell>
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

      {/* 에너지 사용량 등록/수정 다이얼로그 */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingRecord ? '에너지 사용량 수정' : '에너지 사용량 등록'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <FormControl fullWidth margin="normal">
              <InputLabel>에너지 유형</InputLabel>
              <Select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              >
                {energyTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="공급원"
              value={formData.source}
              onChange={(e) => setFormData({ ...formData, source: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="사용량"
              type="number"
              value={formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="위치"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              margin="normal"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={formData.renewable}
                  onChange={(e) => setFormData({ ...formData, renewable: e.target.checked })}
                />
              }
              label="재생에너지"
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

export default Scope2;

