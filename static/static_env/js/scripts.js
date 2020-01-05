/*DOM ready*/
$(document).ready(function(){

		/* Comment */
$('.comment-form').on('submit',function(e){
	e.preventDefault();
	const comment_form_url = $(this).attr('action');
	const comment_form_method = $(this).attr('method');
	let comment_text = $(this).find('.comment-input')[0].value.trim();
	let answer_id 	 = $(this).find('input[name="answer-comment"]')[0].value;
	let comment_count = $(this).parents('.card').find('.card-footer').find('.comment-small span')[0];
	let spinner 		= $(this).find('.loader-span');
	console.log(comment_form_method);
	let request_loads = {
		'answer_id':answer_id,
		'comment_text':comment_text,
		'csrf_token':csrftoken
	}
	// console.log('comment');
	$self = $(this);
	
	spinner.show();/*use a proper spinner*/
	

		$.ajax({
			url : comment_form_url,
			data: request_loads,
			type: 'POST',
			cache:false,
			success:function(response){
				spinner.hide();/*use a proper spinner*/
				comment_count.textContent = parseInt(response.comment_count);
				$self.find('.comment-input')[0].value = "";
			},
			error:function(response){
				console.log(response);
			}
		});
		return false;

  });


/*Answer*/

	$('.answer-form').on('submit',function(e){
		e.preventDefault();
		const answer_form_url = $(this).attr('action');
		let text = $(this).find('.textarea')[0].value.trim();
		let question_id = $(this).find('input[name="question_id"]')[0].value;
		let username 	= $(this).find('#id_answer_by')[0].value;
		let loadr 		= $(this).find('.lds-ellipsis');

		let loads = {
			'username':username,
			'question_id':question_id,
			'text':text,
			'csrf_token':csrftoken
		}

		loadr.show();

		$self = $(this);

		$.ajax({
			url : answer_form_url,
			data: loads,
			type: 'POST',
			cache:false,
			success:function(response){
				$self.find('.textarea')[0].value = '';
				$self.find('.lds-ellipsis').hide();
				console.log(response);
			},
			error:function(response){
				console.log(response);
			}
		});
		return false;


});


/*Connection*/

	$('.connection-form').on('submit',function(e){
		e.preventDefault();
		const follow_url = $(this).attr('action');
		let from_user = $(this).find('input[name="from_user"]')[0];
		let to_user = $(this).find('input[name="to_user"]')[0];
		let btn = $(this).find('.follow-btn');
		let btn_value = btn.attr('value');
		// attr('value','Connected')

		let loadr = {
			'from_user':from_user.value,
			'to_user':to_user.value,
			'csrf_token':csrftoken
		}

		$self = $(this);

		$.ajax({
			url : follow_url,
			data: loadr,
			type: 'POST',
			cache:false,
			success:function(response){
				if(response['is_connected'] == true){
					$self.find('.follow-btn').attr('value','Connected');
					$self.find('.follow-btn').addClass('is-connected');
				}
				else{
					$self.find('.follow-btn').attr('value','Connect');
					$self.find('.follow-btn').removeClass('is-connected');
				}
			},
			error:function(response){
				console.log(response);
			}
		});
		return false;


});


/*Vote*/
/*
Js.
thumbs icon is clicked.
0. thumbs clicked
(check)
1. check with one is clicked and submit its radio button value via ajax
2. * server side login
3. response should change the color of that button

*/

	let vote_radio = $('.thumbs').parents('label').find('input[type="radio"]');
	vote_radio.on('change',function(e){
		choice = $(this).attr('value');
	   // $(this).closest('form').submit();
	   console.log(choice);

    });

});