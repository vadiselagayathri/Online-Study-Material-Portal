function validateSignup(){
  const p=document.getElementById("signupPassword").value;
  const c=document.getElementById("confirmPassword").value;
  if(p.length<6){alert("Password must contain at least 6 characters.");return false}
  if(p!==c){alert("Passwords do not match.");return false}
  return true;
}
function confirmDelete(){return confirm("Are you sure you want to delete this resource?");}
setTimeout(()=>{document.querySelectorAll(".flash").forEach(x=>x.style.display="none")},4000);
document.querySelectorAll(".filter-bar select").forEach(s=>s.addEventListener("change",()=>document.getElementById("filterForm").submit()));
