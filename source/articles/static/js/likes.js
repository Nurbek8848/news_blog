window.onload = function () {


    function getCookieValue(name) {
        const cookies = document.cookie.split('; ');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i];
          const [cookieName, cookieValue] = cookie.split('=');
          if (cookieName === name) {
            console.log(`Found cookie ${name} with value ${cookieValue}`);
            return cookieValue;
          }
        }
        console.log(`Could not find cookie ${name}`);
        return '';
      }

    async function makeRequest(url, method = 'GET', body = null) {

        let headers = {
                'Content-Type': 'application/json',
                // 'X-CSRFToken': getCookieValue('csrftoken'),
                'Authorization': `Token ${getCookieValue('token')}`,
            }

        let requestData = {"method": method, "headers": headers};

        if (body) {
            requestData["body"] = JSON.stringify(body);
        }

        let response = await fetch(url, requestData);
        if (response.ok) {
            return await response.json();
        } else {
            let error = await response.json();
            console.log(error)
        }

    }

    async function testArticle(event) {
        // let url = "http://127.0.0.1:8001/api/v2/articles/";
        let url = event.target.dataset.url;
        let body = {
            "title": "edited 134 1111111 from js",
            "content": "edited 134 1111111 from js",
            "tags": [1]
        }
        let response = await makeRequest(url, "PUT", body);
        console.log(response)
    }

    async function like(event) {
        event.preventDefault();
        let link = event.target;
        let url = link.href;
        let counterId = link.dataset.counterId;
        let counter = document.getElementById(counterId);
        let response = await makeRequest(url, 'POST');
        console.log(response.count);
        counter.innerText = response.count;
    }

    let testDetailBtn = document.getElementById("test-detail-btn");
    let testBtn = document.getElementById("test-btn");
    testBtn.addEventListener('click', testArticle);
    testDetailBtn.addEventListener('click', testArticle);

    let likeLinks = document.querySelectorAll('[data-action="like"]');
    for (let link of likeLinks) {
        link.addEventListener('click', like);
    }


}

