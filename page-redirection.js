const memberstack = window.$memberstackDom

memberstack.getCurrentMember().then((member) => {
  if (member.data) {
    window.location.replace("/member/one-time-contribution");
  }
})