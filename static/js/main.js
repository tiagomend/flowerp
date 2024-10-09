const PrintCard = () => {
  const printableDiv = document.getElementById('card-print');
  if (printableDiv) {
    // Cria uma nova janela para impressão
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>Print Preview</title>
          <link rel="stylesheet" href="/static/css/style.css">
          <link rel="stylesheet" href="/static/icon/style.css">
        </head>
        <body>
          ${printableDiv.innerHTML}
        </body>
      </html>
    `);
    printWindow.document.close();

    printWindow.onload = () => {
      printWindow.print();
    };

    const interval = setInterval(() => {
      if (printWindow.closed) {
        clearInterval(interval);
      } else {
        printWindow.close();
      }
    }, 500);
  }
}

const btnPrint = document.getElementById('btn-print');
if (btnPrint) {
  btnPrint.addEventListener('click', PrintCard);
}


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

  if (!btnTimeSheet) return
  const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

  if (btnTimeSheet) {
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
}

SubmitTimeSheet();


const Awesomplete = () => {
  const awesomplete = [...document.getElementsByClassName('awesomplete')];

  function getDataForOptions(element) {
    const select = element.firstElementChild;
    const options = [...select.getElementsByTagName('option')];
    const data = [];

    for (const option of options) {
      data.push({
        value: option.value,
        textContent: option.textContent
      })
    }
    select.style.visibility = 'hidden';
    select.style.position = 'absolute';
    select.selectedIndex = 0;

    return data;
  }

  function createBoxForOptions() {
    const box = document.createElement('div');
    box.className = 'awesomplete-options';
    return box
  }

  function getRelatedData(data, value) {
    return (
      data.filter(item => {
        return item.textContent.toLowerCase()
          .includes(value.toLowerCase())
      })
    )
  }

  function cleanBox(box) {
    while (box.firstChild) {
      box.removeChild(box.firstChild);
    }
  }

  function getIndex(selectElement, textContent) {
    for (let i = 0; i < selectElement.length; i++) {
      if (selectElement[i].textContent === textContent) {
        return i;
      }
    }
  }

  function createOptionButton(textContent) {
    const option = document.createElement('button');
    option.className = 'awesomplete-btn';
    option.type = 'button';
    option.textContent = textContent;
    return option;
  }

  function createNotOptionButton() {
    const option = document.createElement('button');
    option.className = 'awesomplete-btn';
    option.type = 'button';
    option.innerHTML = `<strong>Nenhuma opção econtrada!</strong>`;
    return option;
  }

  function hideBox(element, box) {
    if (element.contains(box)) {
      element.removeChild(box);
    }
  }

  function showBox(value, filteredOptions, box, element) {
    if (!value) {
      hideBox(element, box);
      return
    }
    if (!filteredOptions.length) {
      const option = createNotOptionButton();
      box.appendChild(option);
      element.appendChild(box);
      return
    }
    filteredOptions.forEach((content) => {
      const option = createOptionButton(content.textContent);
      box.appendChild(option);
      element.appendChild(box);
    });
  }

  awesomplete.forEach(async (element) => {
    const data = getDataForOptions(element);
    const input = document.createElement('input');
    const select = element.firstElementChild;
    input.style.position = 'relative';
    const textContent = select.querySelector('option[selected]').textContent;
    input.value = textContent !== '---------' ? textContent : '';

    element.appendChild(input);
    const box = createBoxForOptions();

    element.addEventListener('input', (e) => {
      const value = e.target.value;
      const filteredOptions = getRelatedData(data, value);
      cleanBox(box);
      const select = element.firstElementChild;
      select.selectedIndex = 0;
      showBox(value, filteredOptions, box, element);
    });

    input.addEventListener('blur', (e) => {
      if (!e.relatedTarget || e.relatedTarget.className !== 'awesomplete-btn') {
        const select = element.firstElementChild;
        select.selectedIndex = getIndex(data, input.value);
        hideBox(element, box);
      }
    });

    box.addEventListener('click', (e) => {
      e.stopPropagation()
      const select = element.firstElementChild;
      input.value = e.target.textContent;
      select.selectedIndex = getIndex(data, e.target.textContent);
      hideBox(element, box);
    });

    window.addEventListener('click', (e) => {
      if (!element.contains(e.target)) {
        hideBox(element, box);
      }
    });

    window.addEventListener('load', (e) => {
      const select = element.firstElementChild;
      select.selectedIndex = getIndex(data, input.value);
      hideBox(element, box);
    });
  });
}

Awesomplete();


const InsertRow = () => {
  const form = document.getElementById('insert_row');
  const button = document.getElementById('insert_row_btn');

  if (form) {
    button.addEventListener('click', () => {
      form.submit();
    })
  }
}

InsertRow();

const Modal = () => {
  const modals = [...document.getElementsByClassName('modal')];

  modals.forEach((modal) => {
    const btnOpenId = modal.getAttribute('data-open');
    const btnCloseId = modal.getAttribute('data-close');
    const btnOpen = document.getElementById(btnOpenId);
    const btnClose = document.getElementById(btnCloseId);
    console.log(modal)

    if (btnOpen) {
      btnOpen.addEventListener('click', (event) => {
        event.preventDefault();
        modal.style.display = 'block';
      });
    }

    if (btnClose) {
      btnClose.addEventListener('click', () => {
        modal.style.display = 'none';
      });
    }
  });
}

Modal();


const SavePurchaseOrder = () => {
  if (document.getElementById("save_form")) {
    let formBase = document.getElementById("form_transaction");
    let btnSave = document.getElementById("save_form");

    btnSave.addEventListener("click", () => {
      let id = btnSave.getAttribute('data-id');
      formBase.action = `/purchases/order/save/${id}/`;
      formBase.submit();
      formBase.action = '';
    });
  }
}

SavePurchaseOrder();
