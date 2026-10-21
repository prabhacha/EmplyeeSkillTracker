import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';
import { BrainCircuit, Users, Award, BookOpen, LayoutDashboard, LogIn, Sparkles, RefreshCw, LogOut, BarChart3, Search, AlertCircle, CheckCircle2 } from 'lucide-react';
import './style.css';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
const NAV = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'employees', label: 'Employees', icon: Users },
  { id: 'skills', label: 'Skills & Certifications', icon: Award },
  { id: 'learning', label: 'Learning plans', icon: BookOpen },
  { id: 'matrix', label: 'Skill Matrix Report', icon: BarChart3 },
];
const asArray = (value) => Array.isArray(value) ? value : (Array.isArray(value?.results) ? value.results : []);
const display = (value) => value === null || value === undefined || value === '' ? '—' : String(value);

function App() {
  const [token, setToken] = useState(localStorage.getItem('access') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [page, setPage] = useState('overview');
  const [employeeId, setEmployeeId] = useState('10');
  const [targetRole, setTargetRole] = useState('Python Full Stack Developer');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [data, setData] = useState({ employees: [], skills: [], certifications: [], employeeCertifications: [], trainings: [], recommendations: [], matrix: [] });

  const client = useMemo(() => axios.create({
    baseURL: API_BASE,
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  }), [token]);

  async function login(e) {
    e.preventDefault(); setError(''); setNotice('');
    try {
      const response = await axios.post(`${API_BASE}/auth/login/`, { username, password });
      const access = response.data.access || response.data.access_token;
      if (!access) throw new Error('Login succeeded but no access token was returned. Check the Django login response.');
      localStorage.setItem('access', access); setToken(access); setNotice('Signed in successfully.');
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || err.message || 'Login failed.');
    }
  }

  function logout() {
    localStorage.removeItem('access'); setToken(''); setResult(null); setData({ employees: [], skills: [], certifications: [], employeeCertifications: [], trainings: [], recommendations: [], matrix: [] }); setPage('overview'); setNotice('You have signed out.'); setError('');
  }

  async function loadPage(target = page) {
    if (!token) return;
    setLoading(true); setError(''); setNotice('');
    try {
      if (target === 'employees') {
        const r = await client.get('/employees/'); setData(d => ({ ...d, employees: asArray(r.data) }));
      } else if (target === 'skills') {
        const [s, c, ec] = await Promise.all([client.get('/skills/'), client.get('/certifications/'), client.get('/employee-certifications/')]);
        setData(d => ({ ...d, skills: asArray(s.data), certifications: asArray(c.data), employeeCertifications: asArray(ec.data) }));
      } else if (target === 'learning') {
        const [t, r] = await Promise.all([client.get('/trainings/'), client.get('/recommendations/')]);
        setData(d => ({ ...d, trainings: asArray(t.data), recommendations: asArray(r.data) }));
      } else if (target === 'matrix') {
        const r = await client.get('/reports/skill-matrix/');
        const rows = asArray(r.data?.results || r.data?.matrix || r.data);
        setData(d => ({ ...d, matrix: rows }));
      }
    } catch (err) {
      if (err.response?.status === 401) setError('Your session may have expired. Please sign in again.');
      else if (err.response?.status === 403) setError('Your account does not have permission to view this section. Try an Admin or Manager account.');
      else setError(err.response?.data?.detail || err.response?.data?.error || `Could not load ${target}. Check that Django is running and the API endpoint is available.`);
    } finally { setLoading(false); }
  }

  useEffect(() => { if (token && page !== 'overview') loadPage(page); }, [token, page]);

  async function recommend(e) {
    e.preventDefault(); setBusy(true); setError(''); setNotice(''); setResult(null);
    try {
      const r = await client.post(`/ai/recommend/${employeeId}/`, { target_role: targetRole }); setResult(r.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.error || JSON.stringify(err.response?.data) || 'Request failed. Ensure Django is running and your account has Admin/Manager permission.');
    } finally { setBusy(false); }
  }

  const filteredEmployees = data.employees.filter(x => `${x.name} ${x.employee_id} ${x.email} ${x.department} ${x.designation}`.toLowerCase().includes(search.toLowerCase()));
  const filteredSkills = data.skills.filter(x => `${x.name} ${x.category} ${x.description}`.toLowerCase().includes(search.toLowerCase()));
  const title = NAV.find(n => n.id === page)?.label || 'Overview';

  function renderOverview() {
    return <>
      <section className="stats">
        <article className="stat"><div className="stat-icon violet"><Users size={20}/></div><span>Employee management</span><strong>{data.employees.length || 'Team directory'}</strong><small>Track people and roles</small></article>
        <article className="stat"><div className="stat-icon blue"><Award size={20}/></div><span>Skills & certifications</span><strong>Skill visibility</strong><small>Monitor proficiency and expiry</small></article>
        <article className="stat"><div className="stat-icon green"><BookOpen size={20}/></div><span>Learning & development</span><strong>Growth roadmap</strong><small>Training based on skill gaps</small></article>
      </section>
      <section className="panel">
        <div className="panel-heading"><div className="ai-mark"><Sparkles size={20}/></div><div><h2>AI Skill Gap & Learning Recommendations</h2><p>Generate a personalized learning plan based on an employee's skills and target role.</p></div></div>
        {!token ? <form className="login-form" onSubmit={login}><div className="notice">Sign in with an existing Django account. The AI recommendation API requires Admin or Manager permission.</div><label>Username<input value={username} onChange={e=>setUsername(e.target.value)} placeholder="Enter username" autoComplete="username" required/></label><label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter password" autoComplete="current-password" required/></label><button className="primary" type="submit"><LogIn size={17}/> Sign in</button></form> : <form className="recommend-form" onSubmit={recommend}><label>Employee database ID<input type="number" min="1" value={employeeId} onChange={e=>setEmployeeId(e.target.value)} required/></label><label>Target role<select value={targetRole} onChange={e=>setTargetRole(e.target.value)}><option>Python Full Stack Developer</option><option>Senior React Developer</option><option>Frontend Developer</option><option>Backend Developer</option></select></label><button className="primary" disabled={busy} type="submit">{busy?<RefreshCw className="spin" size={17}/>:<Sparkles size={17}/>} {busy?'Generating plan…':'Generate AI recommendations'}</button><button className="secondary" type="button" onClick={logout}><LogOut size={16}/> Sign out</button></form>}
        {error&&<div className="error"><AlertCircle size={16}/>{error}</div>}{notice&&<div className="success"><CheckCircle2 size={16}/>{notice}</div>}
        {result&&<div className="results"><div className="result-top"><div><p className="eyebrow">PERSONALIZED DEVELOPMENT PLAN</p><h3>{result.employee?.name||`Employee #${employeeId}`}</h3><p>{result.target_role}</p></div><span className="pill">AI generated</span></div><h4>Skill gaps</h4>{(result.skill_gaps||[]).length?<div className="chips">{result.skill_gaps.map((s,i)=><span className="chip" key={i}>{typeof s==='string'?s:(s.skill||s.name||JSON.stringify(s))}</span>)}</div>:<p className="muted">No skill-gap items were returned.</p>}<h4>Recommendations</h4>{(result.recommendations||[]).map((r,i)=><article className="recommendation" key={i}><div className="rec-title"><b>{r.skill||r.title||`Recommendation ${i+1}`}</b><span className={'priority '+String(r.priority||'medium').toLowerCase()}>{r.priority||'Suggested'}</span></div><p>{r.reason||r.description}</p>{r.learning_steps?.length>0&&<ul>{r.learning_steps.map((s,j)=><li key={j}>{s}</li>)}</ul>}</article>)}<h4>Learning roadmap</h4>{(result.learning_roadmap||[]).map((w,i)=><div className="roadmap" key={i}><span>{w.week||`Week ${i+1}`}</span><div><b>{w.focus||'Learning focus'}</b><p>{w.outcome||w.skills?.join(', ')}</p></div></div>)}</div>}
      </section>
    </>;
  }

  function renderEmployees() {
    return <section className="panel"><div className="section-tools"><div><h2>Employees</h2><p>Employee directory loaded from Django REST API.</p></div><div className="searchbox"><Search size={16}/><input aria-label="Search employees" value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search employees"/></div></div>
      {loading ? <p className="muted">Loading employees…</p> : filteredEmployees.length ? <div className="table-wrap"><table><thead><tr><th>Employee ID</th><th>Name</th><th>Email</th><th>Department</th><th>Designation</th><th>Status</th></tr></thead><tbody>{filteredEmployees.map(e=><tr key={e.id}><td>{display(e.employee_id)}</td><td><b>{display(e.name)}</b></td><td>{display(e.email)}</td><td>{display(e.department)}</td><td>{display(e.designation)}</td><td><span className={e.is_active?'status active-status':'status inactive-status'}>{e.is_active?'Active':'Inactive'}</span></td></tr>)}</tbody></table></div> : <Empty message="No employees found. Add employees through the Django admin or your existing API."/>}
    </section>;
  }

  function renderSkills() {
    return <div className="stacked-panels"><section className="panel"><div className="section-tools"><div><h2>Skills</h2><p>Skill catalogue from the backend.</p></div><div className="searchbox"><Search size={16}/><input aria-label="Search skills" value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search skills"/></div></div>{loading?<p className="muted">Loading skills…</p>:filteredSkills.length?<div className="table-wrap"><table><thead><tr><th>Skill</th><th>Category</th><th>Description</th></tr></thead><tbody>{filteredSkills.map(s=><tr key={s.id}><td><b>{display(s.name)}</b></td><td>{display(s.category)}</td><td>{display(s.description)}</td></tr>)}</tbody></table></div>:<Empty message="No skills found in the catalogue."/>}</section>
      <section className="panel"><div className="section-tools"><div><h2>Certifications</h2><p>Certification catalogue and employee expiry dates.</p></div></div>{data.certifications.length?<div className="table-wrap"><table><thead><tr><th>Certification</th><th>Issuing organization</th><th>Description</th></tr></thead><tbody>{data.certifications.map(c=><tr key={c.id}><td><b>{display(c.name)}</b></td><td>{display(c.issuing_organization)}</td><td>{display(c.description)}</td></tr>)}</tbody></table></div>:<Empty message="No certifications found in the catalogue."/>}
      <h3 className="subheading">Employee certifications</h3>{data.employeeCertifications.length?<div className="table-wrap"><table><thead><tr><th>Employee ID</th><th>Certification ID</th><th>Issue date</th><th>Expiry date</th><th>Certificate number</th></tr></thead><tbody>{data.employeeCertifications.map(c=><tr key={c.id}><td>{display(c.employee)}</td><td>{display(c.certification)}</td><td>{display(c.issue_date)}</td><td>{display(c.expiry_date)}</td><td>{display(c.certificate_number)}</td></tr>)}</tbody></table></div>:<Empty message="No employee certification records found."/>}</section></div>;
  }

  function renderLearning() {
    return <div className="stacked-panels"><section className="panel"><div className="section-tools"><div><h2>Training catalogue</h2><p>Available training options linked to skills.</p></div></div>{loading?<p className="muted">Loading training…</p>:data.trainings.length?<div className="table-wrap"><table><thead><tr><th>Training</th><th>Skill ID</th><th>Provider</th><th>Duration</th><th>Link</th></tr></thead><tbody>{data.trainings.map(t=><tr key={t.id}><td><b>{display(t.name)}</b></td><td>{display(t.skill)}</td><td>{display(t.provider)}</td><td>{display(t.duration)}</td><td>{t.training_url?<a href={t.training_url} target="_blank" rel="noreferrer">Open training ↗</a>:'—'}</td></tr>)}</tbody></table></div>:<Empty message="No training courses found."/>}</section>
      <section className="panel"><div className="section-tools"><div><h2>Training recommendations</h2><p>Recommended learning saved in Django.</p></div></div>{data.recommendations.length?<div className="table-wrap"><table><thead><tr><th>Employee ID</th><th>Training ID</th><th>Reason</th><th>Status</th><th>Recommended date</th></tr></thead><tbody>{data.recommendations.map(r=><tr key={r.id}><td>{display(r.employee)}</td><td>{display(r.training)}</td><td>{display(r.reason)}</td><td><span className="status active-status">{display(r.status)}</span></td><td>{display(r.recommended_date)}</td></tr>)}</tbody></table></div>:<Empty message="No saved training recommendations found. Generate an AI learning plan from Overview to get started."/>}</section></div>;
  }

  function renderMatrix() {
    const rows = data.matrix;
    return <section className="panel"><div className="section-tools"><div><h2>Skill Matrix Report</h2><p>Team skill matrix returned by the reports API.</p></div><button className="secondary" onClick={()=>loadPage('matrix')}><RefreshCw size={15}/> Refresh report</button></div>{loading?<p className="muted">Loading report…</p>:rows.length?<div className="table-wrap"><table><thead><tr>{Object.keys(rows[0] || {}).map(k=><th key={k}>{k.replaceAll('_',' ')}</th>)}</tr></thead><tbody>{rows.map((row,i)=><tr key={row.id||i}>{Object.keys(rows[0]||{}).map(k=><td key={k}>{typeof row[k]==='object'&&row[k]!==null?JSON.stringify(row[k]):display(row[k])}</td>)}</tr>)}</tbody></table></div>:<Empty message="The skill matrix endpoint returned no rows or uses a response format not recognized by this starter UI."/>}</section>;
  }

  return <div className="app"><aside className="sidebar"><div className="brand"><span className="brand-icon"><BrainCircuit size={22}/></span><span>SkillSphere<small>PEOPLE DEVELOPMENT</small></span></div><div className="nav-label">WORKSPACE</div><nav className="nav-list" aria-label="Main navigation">{NAV.map(item=>{const Icon=item.icon;return <button type="button" key={item.id} className={`nav ${page===item.id?'active':''}`} onClick={()=>{setPage(item.id);setSearch('');setError('');setNotice('');}}><Icon size={18}/><span>{item.label}</span></button>;})}</nav><div className="sidebar-bottom"><div className="avatar">ES</div><div><b>{token?'Signed in':'Employee Tracker'}</b><small>{token?'Secure session':'Skill intelligence'}</small></div>{token&&<button className="icon-button" title="Sign out" aria-label="Sign out" onClick={logout}><LogOut size={16}/></button>}</div></aside>
    <main className="main"><header><div><p className="eyebrow">PEOPLE ANALYTICS / {title.toUpperCase()}</p><h1>{page==='overview'?'Employee Skill & Certification Tracker':title}</h1><p className="sub">{page==='overview'?'Understand your team’s capabilities and turn skill gaps into growth plans.':'Browse data managed by your Django REST API.'}</p></div><div className="header-chip"><span className="dot"/> GenAI enabled</div></header>
      {page==='overview'&&renderOverview()}
      {page!=='overview'&&!token&&<section className="panel"><div className="notice">Please sign in on the Overview page to access employee and learning data.</div><button className="primary" onClick={()=>setPage('overview')}><LogIn size={16}/> Go to sign in</button></section>}
      {page==='employees'&&token&&renderEmployees()}
      {page==='skills'&&token&&renderSkills()}
      {page==='learning'&&token&&renderLearning()}
      {page==='matrix'&&token&&renderMatrix()}
      {page!=='overview'&&error&&<div className="error"><AlertCircle size={16}/>{error}</div>}
      {page!=='overview'&&notice&&<div className="success"><CheckCircle2 size={16}/>{notice}</div>}
      <footer>Employee Skill & Certification Tracker <span>React · Django REST Framework · OpenAI</span></footer>
    </main></div>;
}
function Empty({message}) { return <div className="empty-state"><span><Search size={19}/></span><p>{message}</p></div>; }

createRoot(document.getElementById('root')).render(<App/>);
