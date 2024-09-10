const SubmitButton = () => {
  const selector = '[data-btn="form-submit"]';
  const buttons = [...document.querySelectorAll(selector)];

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const dataForm = btn.getAttribute('data-form');
      const form = document.getElementById(dataForm);
      form.submit();
    })
  })
}

SubmitButton();

const NotificationAutoHide = () => {
  const components = [...document.querySelectorAll('.notification')];

  components.forEach((component) => {
    setTimeout(() => {
      component.style.display = 'none';
    }, 10800);
  })
}

NotificationAutoHide();

const FileUploadInput = () => {
  const wrapper = [...document.querySelectorAll('.file-upload-wrapper')];

  wrapper.forEach((component) => {
    const fileInput = component.querySelector('.file-upload-input');
    const fileName = component.querySelector('.file-name');

    fileInput.addEventListener('change', function () {
      fileName.textContent = this.files[0] ? this.files[0].name : 'No file chosen';
    })
  })
}

FileUploadInput();

const TimeSheet = () => {
  const timeSheet = document.getElementById('time_sheet');
  const rows = timeSheet.getElementsByTagName('tr');
  const data = [];

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const cells = row.getElementsByTagName('td');
    const inputs = row.getElementsByTagName('input');

    if (cells.length >= 2 && inputs.length >= 6) {
      const rowData = {
        date: cells[0].innerText,
        first_entry: inputs[0].value,
        first_exit: inputs[1].value,
        second_entry: inputs[2].value,
        second_exit: inputs[3].value,
        third_entry: inputs[4].value,
        third_exit: inputs[5].value,
      }

      data.push([rowData]);
    }
  }
  return data;
}

const SubmitTimeSheet = () => {
  const btnTimeSheet = document.getElementById('btnTimeSheet');
  const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

  btnTimeSheet.addEventListener('click', function () {
    fetch('', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(TimeSheet()),
    })
      .then(response => response.json())
      .then(data => {
        const message = document.createElement('div')
        const html = `
            <div class="notification">
                <div class="message message-success">
                <i class="icon_check"></i>
                ${data.msg}
                </div>
            </div>
            `
        message.innerHTML = html;
        document.body.appendChild(message);

        NotificationAutoHide();
      })
      .catch((error) => {
        console.error('Erro:', error);
      });
  });
}

SubmitTimeSheet();