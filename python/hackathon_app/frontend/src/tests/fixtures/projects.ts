import moment from 'moment'

export default [
  {
    id: 'abc123',
    registrationId: 'abc123',
    title: 'Looker Extension Template',
    description: 'Boilerplate for creating a new Looker Extension',
    dateCreated: moment(0),
    projectType: 'Open',
    contestant: true,
    locked: false,
  },
  {
    id: 'def456',
    registrationId: 'def456',
    title: 'Hackathon registration app',
    description:
      'A web app using a React frontend and a Python flask backend to manage hackathons',
    dateCreated: moment(-100),
    projectType: 'Invite Only',
    contestant: true,
    locked: false,
  },
  {
    id: 'ghi789',
    registrationId: 'ghi789',
    title: 'Chatty',
    description: 'An iframe host/client channel message manager',
    dateCreated: moment(100),
    projectType: 'Closed',
    contestant: false,
    locked: true,
  },
]
