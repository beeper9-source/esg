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
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Factory as FactoryIcon,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface EmissionRecord {
  id: string;
  source: string;
  type: string;
  amount: number;
  unit: string;
  date: string;
  location: string;
}

const Scope1: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState<EmissionRecord | null>(null);
  const [formData, setFormData] = useState({
    source: '',
    type: '',
    amount: '',
    unit: 'tCO2e',
    location: '',
  });

  const [records, setRecords] = useState<EmissionRecord[]>([
    {
      id: '1',
      source: '사무용 차량',
      type: '연료 연소',
      amount: 45.2,
      unit: 'tCO2e',
      date: '2024-01-15',
      location: '본사',
    },
    {
      id: '2',
      source: '보일러',
      type: '연료 연소',
      amount: 120.5,
      unit: 'tCO2e',
      date: '2024-01-14',
      location: '본사',
    },
    {
      id: '3',
      source: '발전기',
      type: '연료 연소',
      amount: 78.3,
      unit: 'tCO2e',
      date: '2024-01-13',
      location: '지점',
    },
  ]);

  const emissionTypes = [
    '연료 연소',
    '공정 배출',
    '냉매 누출',
    '기타 직접 배출',
  ];

  const chartData = [
    { name: '연료 연소', value: 243.7 },
    { name: '공정 배출', value: 45.2 },
    { name: '냉매 누출', value: 12.8 },
    { name: '기타', value: 8.5 },
  ];

  const handleOpen = () => {
    setFormData({
      source: '',
      type: '',
      amount: '',
      unit: 'tCO2e',
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
          ? { ...record, ...formData, amount: parseFloat(formData.amount) }
          : record
      ));
    } else {
      const newRecord: EmissionRecord = {
        id: Date.now().toString(),
        ...formData,
        amount: parseFloat(formData.amount),
        date: new Date().toISOString().split('T')[0],
      };
      setRecords([...records, newRecord]);
    }
    handleClose();
  };

  const handleEdit = (record: EmissionRecord) => {
    setFormData({
      source: record.source,
      type: record.type,
      amount: record.amount.toString(),
      unit: record.unit,
      location: record.location,
    });
    setEditingRecord(record);
    setOpen(true);
  };

  const handleDelete = (id: string) => {
    setRecords(records.filter(record => record.id !== id));
  };

  const totalEmission = records.reduce((sum, record) => sum + record.amount, 0);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Scope 1 - 직접 배출량 관리
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
                <FactoryIcon sx={{ mr: 1, color: 'primary.main' }} />
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
              <Typography variant="h6" gutterBottom>등록된 기록</Typography>
              <Typography variant="h4" color="secondary">
                {records.length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                건
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>전년 대비</Typography>
              <Typography variant="h4" color="success.main">
                -12%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                감소
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>목표 달성률</Typography>
              <Typography variant="h4" color="info.main">
                85%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                달성
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* 배출 유형별 차트 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="배출 유형별 현황" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
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
                  • 전기차 충전소 설치로 연료 연소 감소
                </Typography>
                <Typography variant="body2" gutterBottom>
                  • 보일러 효율 개선으로 배출량 15% 감소
                </Typography>
                <Typography variant="body2" gutterBottom>
                  • 냉매 누출 방지 시스템 구축
                </Typography>
                <Typography variant="body2">
                  • 사무용 차량 전기차 전환 계획 수립
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* 배출량 기록 테이블 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="배출량 기록" />
            <CardContent>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>배출원</TableCell>
                      <TableCell>유형</TableCell>
                      <TableCell>배출량</TableCell>
                      <TableCell>위치</TableCell>
                      <TableCell>날짜</TableCell>
                      <TableCell>액션</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {records.map((record) => (
                      <TableRow key={record.id}>
                        <TableCell>{record.source}</TableCell>
                        <TableCell>
                          <Chip label={record.type} size="small" />
                        </TableCell>
                        <TableCell>{record.amount} {record.unit}</TableCell>
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

      {/* 배출량 등록/수정 다이얼로그 */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingRecord ? '배출량 수정' : '배출량 등록'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <TextField
              fullWidth
              label="배출원"
              value={formData.source}
              onChange={(e) => setFormData({ ...formData, source: e.target.value })}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>배출 유형</InputLabel>
              <Select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              >
                {emissionTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
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

export default Scope1;

