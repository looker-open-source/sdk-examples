import moment from 'moment'

export default [
  {
    id: 'abc123',
    registration_id: 'abc123',
    title: 'Looker Extension Template',
    description: 'Boilerplate for creating a new Looker Extension',
    date_created: new Date(1, 1, 2019),
    project_type: 'Open',
    contestant: true,
    locked: false,
  },
  {
    id: 'def456',
    registration_id: 'def456',
    title: 'Hackathon registration app',
    description:
      'A web app using a React frontend and a Python flask backend to manage hackathons',
    date_created: new Date(6, 6, 2019),
    project_type: 'Invite Only',
    contestant: true,
    locked: false,
  },
  {
    id: 'ghi789',
    registration_id: 'ghi789',
    title: 'Chatty',
    description: 'An iframe host/client channel message manager',
    date_created: new Date(12, 6, 2019),
    project_type: 'Closed',
    contestant: false,
    locked: true,
  },
]
