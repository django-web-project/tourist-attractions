// Edit Review
function editReview(r_id) {
    let editBtn = document.getElementById(`edit-review-btn-${r_id}`)
    let reviewWrapper = document.getElementsByClassName(`review-form-wrapper-${r_id}`)
    let reviewLink = document.getElementById(`review-link-${r_id}`)

    if(reviewWrapper[0].classList.contains('hidden')) {
        reviewWrapper[0].classList.remove('hidden')
        reviewWrapper[1].classList.remove('hidden')
        reviewLink.classList.add('hidden')
        editBtn.classList.add('hidden')
    } else {
        reviewWrapper[0].classList.add('hidden')
        reviewWrapper[1].classList.add('hidden')
        reviewLink.classList.remove('hidden')
        editBtn.classList.remove('hidden')
    }
    return r_id;
}

function saveReview(r_id) {
    editReview(r_id)

    let new_text = $('#review-text-'+r_id).val();
    $.ajax({
        url : '/account/myReviewEdit',
        type : 'get',
        data : {
            review_id : r_id,
            review_text : new_text
        },
        dataType : 'json',
        success : function() {
            console.log('성공');
        },
        error : function() {
            console.log('실패');
        }
    })
    return r_id;
}

function cancelReview(r_id) {
    editReview(r_id);
    return r_id;
}

// Edit Rating
function editRating(r_id) {
    let editBtn = document.getElementById(`edit-rating-btn-${r_id}`)
    let ratingWrapper = document.getElementsByClassName(`rating-form-wrapper-${r_id}`)
    let ratingHeart = document.getElementById(`rating-point-${r_id}`)

    if(ratingWrapper[0].classList.contains('hidden')) {
        ratingWrapper[0].classList.remove('hidden')
        ratingWrapper[1].classList.remove('hidden')
        ratingHeart.classList.add('hidden')
        editBtn.classList.add('hidden')
    } else {
        ratingWrapper[0].classList.add('hidden')
        ratingWrapper[1].classList.add('hidden')
        ratingHeart.classList.remove('hidden')
        editBtn.classList.remove('hidden')
    }
    return r_id
}

function saveRating(r_id) {
    editRating(r_id);
    let new_score = $('#select-rating-'+r_id+' > option:selected').attr('value')
    $.ajax({
        url : '/account/myRatingEdit',
        type : 'get',
        data : {
            rating_id : r_id,
            rating_score : new_score
        },
        dataType : 'json',
        success : function() {
            console.log('성공');
        },
        error : function() {
            console.log('실패');
        }
    })
    return r_id
}

function cancelRating(r_id) {
    editRating(r_id)
    return r_id
}

// Delete  Individual card with X button
function deleteCard(r_id) {
    let result = confirm('정말 삭제하시겠습니까?')
    if(result) {
        let deleteBtn = document.getElementById(`delete-btn-${r_id}`)
        console.log(deleteBtn)
        $(deleteBtn).closest('.card-article').remove();

        $.ajax({
            url: "/account/myListDelete/",
            type: "get",
            data: {
                r_id: r_id
            },
            dataType : 'json',
            success: function() {
                console.log("성공");
            },
            error: function() {
                console.log('실패')
            }
        });
    }
    return r_id;
}

// Delete with Button above
function deleteAll(r_id) {
    let result = confirm('정말 삭제하시겠습니까?')
    let objList = []
    let checkedBox = $('input[type=checkbox]:checked')
    checkedBox.each(function(idx, item) {
        objList.push($(item).attr('data-delete-selection'))

    })
    let json_str = JSON.stringify(objList); // json 문자열화
    console.log(json_str)

    if(result) {
        checkedBox.each(function(idx, item) {
            $(item).closest('.card-article').remove();
        })

        $.ajax({
            url: "/account/deleteAll",
            type: "get",
            data: {
                card_list: json_str
            },
            dataType: 'json',
            success: function() {
                console.log('성공');
            },
            error: function() {
                console.log('실패');
            }
        })
    }
    return r_id
}

// Select All
function changeToCheckbox() {
    let closeIcon = $('.uk-close-large')
    let textBtn = $('.selectAll-btn');
    let checkBox = $('.checkAll-btn');
    let deleteBtn = $('.deleteAll-btn');

    if (closeIcon.hasClass('hidden')) {
        checkBox.addClass('hidden');
        closeIcon.removeClass('hidden');
        textBtn.text('전체선택');
        deleteBtn.prop('disabled', true);
    } else {
        closeIcon.addClass('hidden');
        checkBox.removeClass('hidden');
        textBtn.text('전체선택 해제');
        deleteBtn.prop('disabled', false);
    }
}



// Filtering
function filterCard(u_id) {
    let selectedFilter = $('#filter-review-' + u_id + '> option:selected').attr('value')
    $.ajax({
        url : '/account/myListFilter',
        type : 'get',
        data : {
            user_id : u_id,
            filter_value : selectedFilter,
        },
        dataType : 'json',
        success : function() {
            console.log('성공');
        },
        error : function() {
            console.log('실패');
        }
    })
    return u_id
}




// Heart ratings
// 초기 DB에 저장된 평점
let review_rating = document.getElementsByClassName('hearts-number')
let heartsArray = []
for (let i = 0; i < review_rating.length; i ++) {
    let heartsNum = parseInt(review_rating[i].innerHTML)
    heartsArray.push(heartsNum)
}
console.log(heartsArray)

// 총 평점
const heartsTotal = 5;

// DOM 로딩 됬을 때 getRatings() 함수 실행
document.addEventListener('DOMContentLoaded', getRatings)

// 하트 색 칠하기
function getRatings() {
    for (let number of heartsArray) {
        const heartPercentage = (number / heartsTotal) * 100;

        // Round to nearest 10
        const heartPercentageRounded = `${Math.round(heartPercentage / 10) * 10}%`;
        console.log(heartPercentage)

        // Set width of hearts-inner to percentage
        document.querySelector('.hearts-inner').style.width = heartPercentageRounded;
    }
}



// Text Counter
const newText= document.getElementsByClassName('new-textarea');
const remainingText = document.getElementsByClassName('text-remaining-chars');
const MAX_CHARS = 100;

newText.addEventListener("input", () => {
    const remaining = MAX_CHARS - newText.value.length;
    const color = remaining < MAX_CHARS * 0.1 ? 'red' : null;


    remainingText.textContent = `${remaining}/100`;
    remainingText.style.color = color;
});