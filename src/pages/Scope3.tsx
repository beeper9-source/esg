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
  Stepper,
  Step,
  StepLabel,
  StepContent,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Business as BusinessIcon,
  LocalShipping as ShippingIcon,
  Flight as FlightIcon,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

interface Scope3Record {
  id: string;
  category: string;
  activity: string;
  amount: number;
  unit: string;
  supplier: string;
  date: string;
  status: 'active' | 'reduced' | 'eliminated';
}

const Scope3: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState<Scope3Record | null>(null);
  const [formData, setFormData] = useState({
    category: '',
    activity: '',
    amount: '',
    unit: 'tCO2e',
    supplier: '',
    status: 'active' as 'active' | 'reduced' | 'eliminated',
  });

  const [records, setRecords] = useState<Scope3Record[]>([
    {
      id: '1',
      category: '구매 상품 및 서비스',
      activity: 'IT 장비 구매',
      amount: 450.2,
      unit: 'tCO2e',
      supplier: '삼성전자',
      date: '2024-01-15',
      status: 'active',
    },
    {
      id: '2',
      category: '운송 및 배송',
      activity: '화물 운송',
      amount: 320.5,
      unit: 'tCO2e',
      supplier: '한국통운',
      date: '2024-01-14',
      status: 'reduced',
    },
    {
      id: '3',
      category: '출장',
      activity: '항공 여행',
      amount: 180.3,
      unit: 'tCO2e',
      supplier: '대한항공',
      date: '2024-01-13',
      status: 'active',
    },
    {
      id: '4',
      category: '폐기물 처리',
      activity: '폐기물 처리',
      amount: 95.8,
      unit: 'tCO2e',
      supplier: '환경처리업체',
      date: '2024-01-12',
      status: 'reduced',
    },
  ]);

  const categories = [
    '구매 상품 및 서비스',
    '운송 및 배송',
    '출장',
    '폐기물 처리',
    '임직원 출퇴근',
    '투자',
    '임대 자산',
    '기타',
  ];

  const categoryData = [
    { name: '구매 상품 및 서비스', value: 450.2 },
    { name: '운송 및 배송', value: 320.5 },
    { name: '출장', value: 180.3 },
    { name: '폐기물 처리', value: 95.8 },
    { name: '임직원 출퇴근', value: 120.5 },
    { name: '투자', value: 85.2 },
  ];

  const supplierData = [
    { subject: '탄소중립', A: 85, B: 100, fullMark: 100 },
    { subject: '재생에너지', A: 70, B: 100, fullMark: 100 },
    { subject: '친환경 제품', A: 90, B: 100, fullMark: 100 },
    { subject: '물류 효율', A: 75, B: 100, fullMark: 100 },
    { subject: '폐기물 관리', A: 80, B: 100, fullMark: 100 },
  ];

  const handleOpen = () => {
    setFormData({
      category: '',
      activity: '',
      amount: '',
      unit: 'tCO2e',
      supplier: '',
      status: 'active',
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
      const newRecord: Scope3Record = {
        id: Date.now().toString(),
        ...formData,
        amount: parseFloat(formData.amount),
        date: new Date().toISOString().split('T')[0],
      };
      setRecords([...records, newRecord]);
    }
    handleClose();
  };

  const handleEdit = (record: Scope3Record) => {
    setFormData({
      category: record.category,
      activity: record.activity,
      amount: record.amount.toString(),
      unit: record.unit,
      supplier: record.supplier,
      status: record.status,
    });
    setEditingRecord(record);
    setOpen(true);
  };

  const handleDelete = (id: string) => {
    setRecords(records.filter(record => record.id !== id));
  };

  const totalEmission = records.reduce((sum, record) => sum + record.amount, 0);
  const activeEmission = records.filter(r => r.status === 'active').reduce((sum, record) => sum + record.amount, 0);
  const reducedEmission = records.filter(r => r.status === 'reduced').reduce((sum, record) => sum + record.amount, 0);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Scope 3 - 밸류체인 배출량 관리
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleOpen}
        >
          배출량 등록
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* 요약 카드 */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <BusinessIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">총 배출량</Typography>
              </Box>
              <Typography variant="h4" color="primary">
                {totalEmission.toFixed(1)}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                tCO2e
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>활성 배출량</Typography>
              <Typography variant="h4" color="warning.main">
                {activeEmission.toFixed(1)}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                tCO2e
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>감축된 배출량</Typography>
              <Typography variant="h4" color="success.main">
                {reducedEmission.toFixed(1)}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                tCO2e
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>감축률</Typography>
              <Typography variant="h4" color="info.main">
                {((reducedEmission / totalEmission) * 100).toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                달성
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* 카테고리별 배출량 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="카테고리별 배출량" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoryData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* 공급업체 평가 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="공급업체 친환경 평가" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={supplierData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar name="현재" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                  <Radar name="목표" dataKey="B" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                </RadarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* 밸류체인 개선 로드맵 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="밸류체인 개선 로드맵" />
            <CardContent>
              <Stepper orientation="vertical">
                <Step expanded>
                  <StepLabel>1단계: 공급업체 탄소중립 협약</StepLabel>
                  <StepContent>
                    <Typography variant="body2" gutterBottom>
                      주요 공급업체와 탄소중립 목표 설정 및 협약 체결
                    </Typography>
                    <Chip label="완료" color="success" size="small" />
                  </StepContent>
                </Step>
                <Step expanded>
                  <StepLabel>2단계: 친환경 제품 우선 구매</StepLabel>
                  <StepContent>
                    <Typography variant="body2" gutterBottom>
                      친환경 인증 제품 우선 구매 정책 수립 및 실행
                    </Typography>
                    <Chip label="진행중" color="warning" size="small" />
                  </StepContent>
                </Step>
                <Step expanded>
                  <StepLabel>3단계: 물류 효율화</StepLabel>
                  <StepContent>
                    <Typography variant="body2" gutterBottom>
                      배송 경로 최적화 및 전기차 배송 도입
                    </Typography>
                    <Chip label="계획" color="info" size="small" />
                  </StepContent>
                </Step>
                <Step expanded>
                  <StepLabel>4단계: 디지털 출장 시스템</StepLabel>
                  <StepContent>
                    <Typography variant="body2" gutterBottom>
                      화상회의 시스템 도입으로 출장 횟수 감소
                    </Typography>
                    <Chip label="계획" color="info" size="small" />
                  </StepContent>
                </Step>
              </Stepper>
            </CardContent>
          </Card>
        </Grid>

        {/* 배출량 기록 테이블 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="밸류체인 배출량 기록" />
            <CardContent>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>카테고리</TableCell>
                      <TableCell>활동</TableCell>
                      <TableCell>배출량</TableCell>
                      <TableCell>공급업체</TableCell>
                      <TableCell>상태</TableCell>
                      <TableCell>날짜</TableCell>
                      <TableCell>액션</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {records.map((record) => (
                      <TableRow key={record.id}>
                        <TableCell>{record.category}</TableCell>
                        <TableCell>{record.activity}</TableCell>
                        <TableCell>{record.amount} {record.unit}</TableCell>
                        <TableCell>{record.supplier}</TableCell>
                        <TableCell>
                          <Chip 
                            label={record.status === 'active' ? '활성' : record.status === 'reduced' ? '감축' : '제거'}
                            color={record.status === 'active' ? 'default' : record.status === 'reduced' ? 'warning' : 'success'}
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

      {/* 배출량 등록/수정 다이얼로그 */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingRecord ? '배출량 수정' : '배출량 등록'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <FormControl fullWidth margin="normal">
              <InputLabel>카테고리</InputLabel>
              <Select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              >
                {categories.map((category) => (
                  <MenuItem key={category} value={category}>
                    {category}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="활동"
              value={formData.activity}
              onChange={(e) => setFormData({ ...formData, activity: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="배출량"
              type="number"
              value={formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="공급업체"
              value={formData.supplier}
              onChange={(e) => setFormData({ ...formData, supplier: e.target.value })}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>상태</InputLabel>
              <Select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value as 'active' | 'reduced' | 'eliminated' })}
              >
                <MenuItem value="active">활성</MenuItem>
                <MenuItem value="reduced">감축</MenuItem>
                <MenuItem value="eliminated">제거</MenuItem>
              </Select>
            </FormControl>
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

export default Scope3;

