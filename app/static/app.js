const state = { people: [] };
const $ = (selector) => document.querySelector(selector);

async function api(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {'Content-Type': 'application/json', ...(options.headers || {})}
  });
  if (response.status === 401) {
    location.replace('/login');
    throw new Error('로그인이 필요합니다.');
  }
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || '요청을 처리하지 못했습니다.');
  }
  return response.status === 204 ? null : response.json();
}

function toast(message, isError = false) {
  const element = $('#toast');
  element.textContent = message;
  element.className = `toast show${isError ? ' error' : ''}`;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => element.className = 'toast', 2200);
}

function escapeHtml(value) {
  const node = document.createElement('span');
  node.textContent = value;
  return node.innerHTML;
}

function genderLabel(gender) {
  return {Male: '남성', Female: '여성'}[gender] || gender;
}

function render() {
  $('#people').innerHTML = state.people.map(person => `
    <tr>
      <td data-label="이름" class="person-name">${escapeHtml(person.name)}</td>
      <td data-label="성별"><span class="badge ${person.gender.toLowerCase()}">${genderLabel(person.gender)}</span></td>
      <td data-label="나이">${person.age}세</td>
      <td data-label="작업" class="row-actions">
        <button class="icon-btn" data-action="edit" data-id="${person.id}" aria-label="${escapeHtml(person.name)} 수정">✎ 수정</button>
        <button class="icon-btn danger" data-action="delete" data-id="${person.id}" aria-label="${escapeHtml(person.name)} 삭제">⌫ 삭제</button>
      </td>
    </tr>`).join('');
  $('#total').textContent = state.total;
  $('#empty').style.display = state.people.length ? 'none' : 'block';
}

async function loadPeople() {
  const data = await api(`/api/members?q=${encodeURIComponent($('#search').value.trim())}`);
  state.people = data.items;
  state.total = data.total;
  render();
}

function openModal(person = null) {
  $('#modal-title').textContent = person ? '사용자 수정' : '사용자 추가';
  $('#person-id').value = person?.id || '';
  $('#name').value = person?.name || '';
  $('#gender').value = person?.gender || 'Male';
  $('#age').value = person?.age ?? '';
  $('#modal').classList.add('open');
  setTimeout(() => $('#name').focus(), 0);
}

function closeModal() {
  $('#modal').classList.remove('open');
  $('#person-form').reset();
}

async function initialize() {
  try {
    const [account, meta] = await Promise.all([api('/api/auth/me'), api('/api/system/meta')]);
    $('#welcome-name').textContent = account.username;
    $('#avatar').textContent = account.username[0].toUpperCase();
    $('#server-ip').textContent = meta.server_ip || '감지 실패';
    $('#server-name').textContent = meta.server_name;
    $('#ip').textContent = meta.ip;
    $('#xff').textContent = meta.xff;
    await loadPeople();
  } catch (error) {
    if (!location.pathname.startsWith('/login')) toast(error.message, true);
  }
}

$('#add').addEventListener('click', () => openModal());
$('#cancel').addEventListener('click', closeModal);
$('#modal').addEventListener('click', event => { if (event.target === $('#modal')) closeModal(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeModal(); });

let searchTimer;
$('#search').addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => loadPeople().catch(err => toast(err.message, true)), 250);
});

$('#people').addEventListener('click', async event => {
  const button = event.target.closest('button[data-action]');
  if (!button) return;
  const id = Number(button.dataset.id);
  const person = state.people.find(item => item.id === id);
  if (button.dataset.action === 'edit') return openModal(person);
  if (!confirm(`"${person.name}" 사용자를 삭제하시겠습니까?`)) return;
  try {
    await api(`/api/members/${id}`, {method: 'DELETE'});
    toast('사용자를 삭제했습니다.');
    await loadPeople();
  } catch (error) { toast(error.message, true); }
});

$('#person-form').addEventListener('submit', async event => {
  event.preventDefault();
  const id = $('#person-id').value;
  const payload = {
    name: $('#name').value.trim(),
    gender: $('#gender').value,
    age: Number($('#age').value)
  };
  try {
    await api(id ? `/api/members/${id}` : '/api/members', {
      method: id ? 'PUT' : 'POST',
      body: JSON.stringify(payload)
    });
    closeModal();
    toast(id ? '사용자 정보를 수정했습니다.' : '새 사용자를 추가했습니다.');
    await loadPeople();
  } catch (error) { toast(error.message, true); }
});

$('#logout').addEventListener('click', async () => {
  await api('/api/auth/logout', {method: 'POST'});
  location.replace('/login');
});

initialize();
