# Q&A system

## Requirement

User can store their own documents and generate the personalized Q&A.

The document only need support markdown format.

## User Interface

### Dashboard

- A navigation tabs switch between documents page and Q&A page

- A grid for listing out all the documents.
    - Items in the grid serves as the documents which the user has been created.
        - User can click the item to navigate to the editor for editing.
        - every items also have a button on the top-right for deleting the document.
    - An empty item with a plus icon,
      user can click it to navigate to the editor for creating new document.

### Editor

- A textarea that user can write their document.

- A submit button for saving.

### Q&A

- An input below which user can type any questions.

- A submit button for submit the question.

- The answer based on the documents will be shown on the top of the page.

- The related citations will be shown below the answer,
  only need to display the top 3 related.

## API

### Upload document

```http
POST /documents
content-type: multipart/form-data; boundary=<boundary>

--<boundary>
content-disposition: form-data; name="file"; filename="<filename>.md"
content-type: text/plain

(content of the uploaded file <filename>.md)
--<boundary>--
```

```json
{
    data: {
        id: <string>,
        name: <string>,
        src: <string>
    }
}
```

### Get all document

```http
GET /documents
content-type: application/json
```

```json
{
    data: [
        {
            id: <string>,
            name: <string>,
            src: <string>
        },
        ...
    ]
}
```

### Get document

```http
GET /documents/:document-id
content-type: application/json
```

```json
{
    data: {
        id: <string>,
        name: <string>,
        src: <string>
    }
}
```

### Edit document

```http
PUT /documents/:document-id
content-type: multipart/form-data; boundary=<boundary>

--<boundary>
content-disposition: form-data; name="file"; filename="<filename>.md"
content-type: text/plain

(content of the uploaded file <filename>.md)
--<boundary>--
```

```json
{
    data: {
        id: <string>,
        name: <string>,
        src: <string>
    }
}
```

### Delete document

```http
DELETE /documents/:document-id
```

```json
{
    data: "ok"
}
```

### Submit one shot q&a

```http
POST /questions
content-type: application/x-www-form-urlencoded

query=<string>
```

```text
<answer>
```

