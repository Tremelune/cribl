import React, { useState } from 'react';

export default function SearchForm() {
    const [results, setResults] = useState(null);
    const [fullUrl, setFullUrl] = useState(null);
    const [filename, setFilename] = useState(null);

    function search(event) {
        const BASE_PREVIEW_URL = "http://127.0.0.1:5000/logs/previews"
        const BASE_FULL_URL = "http://127.0.0.1:5000/logs"

        let filename = event.target.filename.value
        let limit = event.target.limit.value
        let filter = event.target.filter.value

        let query = "?filename=" + filename
        if (limit) {
            query += "&limit=" + limit
        }
        if (filter) {
            query += "&filter=" + filter
        }

        console.log(query)

        fetch(BASE_PREVIEW_URL + query)
            .then(response => response.json())
            .then(data => setResults(data))
            .then(() => setFullUrl(BASE_FULL_URL + query))
            .catch(error => console.error(error));

        event.preventDefault();
    }

    let lines = ""
    if(results) {
        lines = results.map((line, index) => <li key={index}>{line}</li>)
    }

    let isDownloadHidden = true
    if(fullUrl) {
        isDownloadHidden = false
    }

    return (
        <div>
            <form onSubmit={search}>
                Filename: <input name="filename" type="text" required /><br />
                Limit (optional): <input name="limit" type="text" /><br />
                Filter (optional): <input name="filter" type="text" /><br />
                <button type="submit">Get Preview</button>
            </form>

            Results<br />
            <div hidden={isDownloadHidden}>
                <a href={fullUrl} download target="_blank">[download]</a>
            </div>
            <div className="results"><ul>{lines}</ul></div>
        </div>
    );
}
