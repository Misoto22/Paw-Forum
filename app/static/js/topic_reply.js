document.addEventListener('DOMContentLoaded', function() {
  // Get references to the necessary elements
  const submitReplyButton = document.querySelector('#submitReplyBtn');
  const repliesContainer = document.querySelector('.replies');

  // Event listener for the submit reply button
  submitReplyButton.addEventListener('click', function() {
    const replyForm = document.querySelector('.reply-form');
    const replyText = replyForm.querySelector('textarea').value;
    if (replyText.trim() !== '') {
      const newReply = createReplyElement(replyText);
      repliesContainer.appendChild(newReply);
      replyForm.querySelector('textarea').value = '';
    }
  });

  // Event listener for the replies container
  repliesContainer.addEventListener('click', function(event) {
    // Check if the clicked element is a reply button
    if (event.target.classList.contains('reply-button')) {
      const replyElement = event.target.closest('.reply');
      const nestedReplyForm = replyElement.querySelector('.nested-reply-form');
      // Toggle the visibility of the nested reply form
      nestedReplyForm.style.display = nestedReplyForm.style.display === 'none' ? 'block' : 'none';
    }
    // Check if the clicked element is a submit nested reply button
    if (event.target.classList.contains('submit-nested-reply')) {
      const nestedReplyForm = event.target.closest('.nested-reply-form');
      const replyText = nestedReplyForm.querySelector('textarea').value;
      if (replyText.trim() !== '') {
        const newReply = createReplyElement(replyText);
        nestedReplyForm.parentElement.appendChild(newReply);
        nestedReplyForm.querySelector('textarea').value = '';
        nestedReplyForm.style.display = 'none';
      }
    }
  });

  // Function to create a new reply element
  function createReplyElement(replyText) {
    const replyElement = document.createElement('div');
    replyElement.classList.add('reply');

    const currentTime = new Date().toLocaleString(); // Get current time

    replyElement.innerHTML = `
      <div class="reply-header">
        <img src="../../image/avatar.png" alt="User Avatar" class="reply-avatar" />
        <span class="reply-username">Username</span>
        <span class="reply-time">${currentTime}</span>
      </div>
      <div class="reply-content">
        ${replyText}
      </div>
      <div class="reply-footer">
        <button class="reply-button">Reply</button>
      </div>
      <div class="nested-reply-form">
        <textarea placeholder="Write your reply..."></textarea>
        <button class="submit-nested-reply">Submit Reply</button>
      </div>
    `;
    return replyElement;
  }
});