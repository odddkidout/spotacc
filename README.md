
# Account Manager
A Webapp to manage database of login details and session for a platform.


## API Reference

#### Get a single acc

```http
  GET /api/acc
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  PUT /api/acc?_id={id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


```
// data to update
{
    "InUse":true,
    etc
}
```



