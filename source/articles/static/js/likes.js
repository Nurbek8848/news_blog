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
        console.log(method);

        let headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookieValue('csrftoken'),
                'Cookie': 'sessionid=rsy57jzzlorvm307iecavoch1x01a0t0'
            }

        let requestData = {"method": method, "headers": headers};

        if (body) {
            requestData["body"] = JSON.stringify(body);
        }

        let response = await fetch(url, requestData);
        return await response.json();
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

    let likeLinks = document.querySelectorAll('[data-action="like"]');
    for (let link of likeLinks) {
        link.addEventListener('click', like);
    }


}

