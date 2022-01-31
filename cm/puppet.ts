import * as puppeteer from 'puppeteer';
import * as fs from 'fs';

(async () => {
  const browser = await puppeteer.launch({headless: false, slowMo: 400});
  const page = await browser.newPage();
  await page.goto('https://www.coolermaster.com/catalog/cases/?filter=8448/#!/Size=Mid%20Tower');
  let cases = await page.evaluate(findCases)
  let caseData: {}[] = []
  for (let i = 0; i < cases.length; i++) {
    await page.goto(cases[i]);

    let resp = await page.evaluate(parseCase)
    caseData.push(resp)
  }
  saveData("coolermaster.json", caseData)
  
  await browser.close();
})();

function findCases (): string[] {
  const casePathSelector = 'div#product-overview-container div.card__img a';
  let caseUrlNodes = document.querySelectorAll(casePathSelector) as NodeListOf<HTMLAnchorElement>;
  console.log(`Found ${caseUrlNodes.length} cases`)
  let caseUrls = Array.from(caseUrlNodes).map(a => a.href)
  return caseUrls
}

function parseCase (): {} {
  const tableCells = document.querySelectorAll("table.compare-table td td") as NodeListOf<HTMLElement>
  let data: {[key: string]: string} = {};
  for (let i = 0; i < tableCells.length; i+= 2){
      data[tableCells[i].innerText] = tableCells[i+1].innerText
  }
  data['name'] = document.querySelector("head title")!.innerHTML
  return data  
}


function saveData(filename: string, data: any) {
  fs.writeFile(filename, JSON.stringify(data), function (err) {
      if (err) throw err;
      console.log('Replaced!');
    });
}
