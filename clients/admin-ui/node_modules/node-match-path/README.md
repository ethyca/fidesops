[![Package version](https://img.shields.io/npm/v/node-match-path.svg)](https://npmjs.com/package/node-match-path)

# `node-match-path`

Matches a URL against the given path.

## Getting started

### Install

```bash
npm install node-match-path
```

## Usage

```js
const { match } = require('node-match-path')

match('/user/:userId', '/user/5')
/*
{
  matches: true,
  params: {
    userId: '5'
  }
}
*/
```

## API

### `match(path: RegExp | string, url: string): Match`

Returns a match data, if any, between a url and a path.

#### String path

```js
match('/admin', '/admin')

/*
{
  matches: true,
  params: null
}
*/
```

#### Path parameters

```js
match('/admin/:messageId', '/admin/abc-123')

/*
{
  matches: true,
  params: {
    messageId: 'abc-123'
  }
}
*/
```

#### Wildcard

```js
match('/user/*/inbox', '/user/abc-123/inbox')

/*
{
  matches: true,
  params: null
}
*/
```

#### Regular expression

```js
match(/\/messages\/.+?\/participants/, '/messages/5/participants')

/*
{
  matches: true,
  params: null
}
*/
```

## Honorable mentions

- [`path-to-regexp`](https://github.com/pillarjs/path-to-regexp)
