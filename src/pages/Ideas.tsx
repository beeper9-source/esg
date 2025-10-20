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
  Rating,
  Avatar,
  Badge,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Lightbulb as LightbulbIcon,
  ThumbUp as ThumbUpIcon,
  Comment as CommentIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface Idea {
  id: string;
  title: string;
  description: string;
  category: string;
  author: string;
  department: string;
  status: 'submitted' | 'reviewing' | 'approved' | 'implemented' | 'rejected';
  priority: 'low' | 'medium' | 'high';
  impact: number;
  feasibility: number;
  likes: number;
  comments: number;
  date: string;
  implementationDate?: string;
}

const Ideas: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [editingIdea, setEditingIdea] = useState<Idea | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    department: '',
    priority: 'medium' as 'low' | 'medium' | 'high',
  });

  const [ideas, setIdeas] = useState<Idea[]>([
    {
      id: '1',
      title: '사무용 전기차 충전소 확대',
      description: '사무실 주차장에 전기차 충전소를 추가로 설치하여 직원들의 전기차 사용을 촉진하고 Scope 1 배출량을 감소시킬 수 있습니다.',
      category: 'Scope 1',
      author: '김철수',
      department: 'IT개발팀',
      status: 'implemented',
      priority: 'high',
      impact: 4,
      feasibility: 5,
      likes: 15,
      comments: 8,
      date: '2024-01-10',
      implementationDate: '2024-01-20',
    },
    {
      id: '2',
      title: '스마트 조명 시스템 도입',
      description: 'IoT 센서를 활용한 자동 조명 시스템으로 전력 사용량을 30% 절약할 수 있습니다.',
      category: 'Scope 2',
      author: '이영희',
      department: '시설관리팀',
      status: 'approved',
      priority: 'medium',
      impact: 3,
      feasibility: 4,
      likes: 12,
      comments: 5,
      date: '2024-01-12',
    },
    {
      id: '3',
      title: '공급업체 친환경 인증 제도',
      description: '공급업체에 친환경 인증을 요구하여 Scope 3 배출량을 감소시킬 수 있습니다.',
      category: 'Scope 3',
      author: '박민수',
      department: '구매팀',
      status: 'reviewing',
      priority: 'high',
      impact: 5,
      feasibility: 3,
      likes: 18,
      comments: 12,
      date: '2024-01-15',
    },
    {
      id: '4',
      title: '폐기물 업사이클링 프로그램',
      description: '사무용품을 업사이클링하여 새로운 제품으로 재생산하는 프로그램을 제안합니다.',
      category: '순환경제',
      author: '정수진',
      department: '환경팀',
      status: 'submitted',
      priority: 'medium',
      impact: 4,
      feasibility: 4,
      likes: 9,
      comments: 3,
      date: '2024-01-18',
    },
  ]);

  const categories = [
    'Scope 1',
    'Scope 2',
    'Scope 3',
    '순환경제',
    '기타',
  ];

  const departments = [
    'IT개발팀',
    '시설관리팀',
    '구매팀',
    '환경팀',
    '마케팅팀',
    '인사팀',
    '기타',
  ];

  const statusData = [
    { name: '제출됨', value: ideas.filter(i => i.status === 'submitted').length },
    { name: '검토중', value: ideas.filter(i => i.status === 'reviewing').length },
    { name: '승인됨', value: ideas.filter(i => i.status === 'approved').length },
    { name: '구현됨', value: ideas.filter(i => i.status === 'implemented').length },
    { name: '거부됨', value: ideas.filter(i => i.status === 'rejected').length },
  ];

  const categoryData = [
    { name: 'Scope 1', value: ideas.filter(i => i.category === 'Scope 1').length },
    { name: 'Scope 2', value: ideas.filter(i => i.category === 'Scope 2').length },
    { name: 'Scope 3', value: ideas.filter(i => i.category === 'Scope 3').length },
    { name: '순환경제', value: ideas.filter(i => i.category === '순환경제').length },
  ];

  const handleOpen = () => {
    setFormData({
      title: '',
      description: '',
      category: '',
      department: '',
      priority: 'medium',
    });
    setEditingIdea(null);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingIdea(null);
  };

  const handleSubmit = () => {
    if (editingIdea) {
      setIdeas(ideas.map(idea => 
        idea.id === editingIdea.id 
          ? { ...idea, ...formData }
          : idea
      ));
    } else {
      const newIdea: Idea = {
        id: Date.now().toString(),
        ...formData,
        author: '현재 사용자',
        status: 'submitted',
        impact: 3,
        feasibility: 3,
        likes: 0,
        comments: 0,
        date: new Date().toISOString().split('T')[0],
      };
      setIdeas([...ideas, newIdea]);
    }
    handleClose();
  };

  const handleEdit = (idea: Idea) => {
    setFormData({
      title: idea.title,
      description: idea.description,
      category: idea.category,
      department: idea.department,
      priority: idea.priority,
    });
    setEditingIdea(idea);
    setOpen(true);
  };

  const handleDelete = (id: string) => {
    setIdeas(ideas.filter(idea => idea.id !== id));
  };

  const handleLike = (id: string) => {
    setIdeas(ideas.map(idea => 
      idea.id === id 
        ? { ...idea, likes: idea.likes + 1 }
        : idea
    ));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'submitted': return 'default';
      case 'reviewing': return 'warning';
      case 'approved': return 'info';
      case 'implemented': return 'success';
      case 'rejected': return 'error';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'default';
    }
  };

  const totalIdeas = ideas.length;
  const implementedIdeas = ideas.filter(i => i.status === 'implemented').length;
  const totalLikes = ideas.reduce((sum, idea) => sum + idea.likes, 0);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          임직원 아이디어
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleOpen}
        >
          아이디어 제안
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* 요약 카드 */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <LightbulbIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">총 아이디어</Typography>
              </Box>
              <Typography variant="h4" color="primary">
                {totalIdeas}
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
              <Typography variant="h6" gutterBottom>구현된 아이디어</Typography>
              <Typography variant="h4" color="success.main">
                {implementedIdeas}
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
              <Typography variant="h6" gutterBottom>총 좋아요</Typography>
              <Typography variant="h4" color="info.main">
                {totalLikes}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                개
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>구현률</Typography>
              <Typography variant="h4" color="warning.main">
                {((implementedIdeas / totalIdeas) * 100).toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                달성률
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* 상태별 아이디어 분포 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="상태별 아이디어 분포" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={statusData}>
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

        {/* 카테고리별 아이디어 분포 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="카테고리별 아이디어 분포" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoryData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* 인기 아이디어 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="인기 아이디어 TOP 3" />
            <CardContent>
              <Grid container spacing={2}>
                {ideas
                  .sort((a, b) => b.likes - a.likes)
                  .slice(0, 3)
                  .map((idea, index) => (
                    <Grid item xs={12} md={4} key={idea.id}>
                      <Box sx={{ p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Avatar sx={{ mr: 1, bgcolor: 'primary.main' }}>
                            {index + 1}
                          </Avatar>
                          <Typography variant="h6">{idea.title}</Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {idea.description.substring(0, 100)}...
                        </Typography>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Chip label={idea.category} size="small" />
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <ThumbUpIcon sx={{ mr: 0.5, fontSize: 16 }} />
                            <Typography variant="body2">{idea.likes}</Typography>
                          </Box>
                        </Box>
                      </Box>
                    </Grid>
                  ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* 아이디어 목록 테이블 */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="아이디어 목록" />
            <CardContent>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>제목</TableCell>
                      <TableCell>카테고리</TableCell>
                      <TableCell>제안자</TableCell>
                      <TableCell>부서</TableCell>
                      <TableCell>상태</TableCell>
                      <TableCell>우선순위</TableCell>
                      <TableCell>영향도</TableCell>
                      <TableCell>실현가능성</TableCell>
                      <TableCell>좋아요</TableCell>
                      <TableCell>액션</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {ideas.map((idea) => (
                      <TableRow key={idea.id}>
                        <TableCell>
                          <Typography variant="subtitle2">{idea.title}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {idea.description.substring(0, 50)}...
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip label={idea.category} size="small" />
                        </TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <PersonIcon sx={{ mr: 1, fontSize: 16 }} />
                            {idea.author}
                          </Box>
                        </TableCell>
                        <TableCell>{idea.department}</TableCell>
                        <TableCell>
                          <Chip 
                            label={idea.status === 'submitted' ? '제출됨' : 
                                   idea.status === 'reviewing' ? '검토중' :
                                   idea.status === 'approved' ? '승인됨' :
                                   idea.status === 'implemented' ? '구현됨' : '거부됨'}
                            color={getStatusColor(idea.status)}
                            size="small" 
                          />
                        </TableCell>
                        <TableCell>
                          <Chip 
                            label={idea.priority === 'low' ? '낮음' : 
                                   idea.priority === 'medium' ? '보통' : '높음'}
                            color={getPriorityColor(idea.priority)}
                            size="small" 
                          />
                        </TableCell>
                        <TableCell>
                          <Rating value={idea.impact} readOnly size="small" />
                        </TableCell>
                        <TableCell>
                          <Rating value={idea.feasibility} readOnly size="small" />
                        </TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <IconButton size="small" onClick={() => handleLike(idea.id)}>
                              <ThumbUpIcon />
                            </IconButton>
                            <Typography variant="body2">{idea.likes}</Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <IconButton onClick={() => handleEdit(idea)}>
                            <EditIcon />
                          </IconButton>
                          <IconButton onClick={() => handleDelete(idea.id)}>
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

      {/* 아이디어 등록/수정 다이얼로그 */}
      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingIdea ? '아이디어 수정' : '아이디어 제안'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <TextField
              fullWidth
              label="제목"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="설명"
              multiline
              rows={4}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              margin="normal"
            />
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
            <FormControl fullWidth margin="normal">
              <InputLabel>부서</InputLabel>
              <Select
                value={formData.department}
                onChange={(e) => setFormData({ ...formData, department: e.target.value })}
              >
                {departments.map((department) => (
                  <MenuItem key={department} value={department}>
                    {department}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth margin="normal">
              <InputLabel>우선순위</InputLabel>
              <Select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value as 'low' | 'medium' | 'high' })}
              >
                <MenuItem value="low">낮음</MenuItem>
                <MenuItem value="medium">보통</MenuItem>
                <MenuItem value="high">높음</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>취소</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingIdea ? '수정' : '제안'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Ideas;

