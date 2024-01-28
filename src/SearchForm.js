import { ErrorBoundary } from "react-error-boundary";
import React, { useState } from 'react';

export default function SearchForm() {
    const [results, setResults] = useState(null);

    function search(event) {
        // console.log('form sumtit')
        // console.log(event)
        const BASE_URL = "http://127.0.0.1:5000/logs/previews"

        let filename = event.target.filename.value
        let limit = event.target.limit.value
        let filter = event.target.filter.value

        let query = BASE_URL + "?filename=" + filename
        if (limit) {
            query += "&limit=" + limit
        }
        if (filter) {
            query += "&filter=" + filter
        }

        console.log(query)

        fetch(query)
            .then(response => response.json())
            .then(data => setResults(data))
            .catch(error => console.error(error));

        event.preventDefault();
    }

    let lines = ""
    if(results) {
        lines = results.map((line, index) => <li key={index}>{line}</li>)
    }

    return (
        <div>
            <form onSubmit={search}>
                Filename: <input name="filename" type="text" required /><br />
                Limit (optional): <input name="limit" type="text" /><br />
                Filter (optional): <input name="filter" type="text" /><br />
                <button type="submit">Search</button>
            </form>

            Results<br/>
            <div class="results">
                <ErrorBoundary fallback={<p>There was an error while submitting the form</p>}>
                    <ul>{lines}</ul>
                </ErrorBoundary>
            </div>
        </div>
    );
}
