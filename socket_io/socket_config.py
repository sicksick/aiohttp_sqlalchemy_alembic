users_socket = dict()

ROUTES = {
    'FRONT': {
        'CONNECT': 'connect',
        'DISCONNECT': 'disconnect',
        'AUTH': 'auth',
        'USER': {
            'ONLINE': 'user:online'
        },
        'CHAT': {
            'STATUS': 'chat:status',
            'MESSAGE': {
                'HISTORY': 'chat:message:history',
                'NEW': 'chat:message:new'
            }
        }
    },
    'BACK': {
        'CONNECT': 'connect',
        'DISCONNECT': 'disconnect',
        'MY_EVENT': 'my_event',
        'USER': {
            'INVITE': 'user:invite',
            'EXCLUDE': 'user:exclude'
        },
        'CHAT': {
            'CREATE': 'chat:create',
            'REMOVE': 'chat:remove',
            'INVITE': 'chat:invite',
            'MESSAGE': {
                'SEND': 'chat:message:send',
                'EDIT': 'chat:message:edit',
                'REMOVE': 'chat:message:remove',
            }
        },
    }
}
