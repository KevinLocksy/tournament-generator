function setLinkTableRow(elementID, domainSubDir){
  const list_rows = document.getElementById(elementID).rows;
  console.log(list_rows)
  for (let i = 1; i < list_rows.length; i++) {
    const row = list_rows[i];
    const rowID = row.getAttribute("data-index");
    row.addEventListener("click", () => {
      window.location.href = domainSubDir+rowID;
    });
  }
}