# API REST with Python Tornado e Mongodb
The purpose of this test is to develop a **CRUD** to facilitate the management of employees of a technology company.

In the employee registration form on the front end of the application, you have the following fields to fill in:
- Name (text)*
- Birth Date (date picker)*
- Gender*
- Email*
- CPF*
- Start Date (MM/YYYY)*
- Team (Mobile, Frontend, Backend ou null)

Fields with * are mandatory!

| Action | HTTP | PAYLOAD | URL | Descripition |
| --- | --- | --- | --- | --- |
| Create | POST | json | /employee | Create a employee entity with this payload |
| Read | GET | - | /employee | Get all employee entities from the resource |
| Read | GET | - | /employee/:id | Get a single nutemployee entity |
| Update | PUT | json | /employee/:id | Update a employee entity with this payload |
| Delete | DELETE | - | /employee/:id | Delete a employee entity |

Payload must be include as body json raw and formatted like below, you are free to include any desired propety:

```json
{
	"name":"Fulano de tal",
	"gender":"Male",
	"email":"fulanodetal@mail.com"
	...
}

```
