$(document).ready(function () {
    $('#btn-save-home, #btn-save-about, #btn-save-contact').click(PortfolioPost);
});

function PortfolioPost() {
    const crf = $('input[name=csrfmiddlewaretoken]').val();
    const PostUrl = $('input[name=post-url]').val();

    // Gather form data
    let formData = new FormData();
    formData.append('first_name', $('#first-name').val());
    formData.append('last_name', $('#last-name').val());
    formData.append('profile_image', $('#profile-image')[0].files[0]);
    formData.append('user_skill_title', $('#user-skill-title').val());
    formData.append('introduce', $('#introduce').val());
    formData.append('about_me_title', $('#about-me-title').val());
    formData.append('work_experience', $('#work-experience').val());
    formData.append('birthday', $('#birthday').val());
    formData.append('website', $('#website').val());
    formData.append('freelance', $('#freelance').val());
    formData.append('phone', $('#phone').val());
    formData.append('linkedin', $('#linkedin').val());
    formData.append('instagram', $('#instagram').val());

    // Determine the type of saving process
    let savingProcess = '';
    let clickedButton = $(this);
    if (clickedButton.text() === 'Save') {
        savingProcess = true;
    }
    clickedButton.text('Saving');

    // Make AJAX request
    $.ajax({
        url: PostUrl,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': crf
        },
        success: function(response) {
            // Handle success
            clickedButton.text('Save');
            // Do something with the response
        },
        error: function(xhr, status, error) {
            // Handle error
            alert('Error: ' + error);
            window.location.reload(); // Reload the page on error
        }
    });
}
