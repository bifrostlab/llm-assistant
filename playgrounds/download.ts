import { download } from '../src/slash-commands/review-resume/downloader';
import { getOutputFileName } from '../src/slash-commands/review-resume/utils';

async function downloadGDrive() {
  const output = getOutputFileName('gdrive');
  await download('https://drive.google.com/file/d/1W8wHR_OqRTr7N9A674tbNWtObN6RvwmE/view?usp=sharing', output);
}

async function downloadGeneric() {
  const output = getOutputFileName('generic');
  await download('https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf', output);
}

async function go() {
  await downloadGDrive();
  await downloadGeneric();
}
go();
