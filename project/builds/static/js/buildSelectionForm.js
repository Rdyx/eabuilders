document.addEventListener('DOMContentLoaded', function() {
   document.querySelectorAll('select.text-center.px-3').forEach(element => test(element));
}, false);



function test(e) {
    target_div = document.getElementById(e.name)
    target_img = document.getElementById(e.name+'_img')
    target_name = document.getElementById(e.name+'_name')
    target_desc = document.getElementById(e.name+'_desc')
    target_range = document.getElementById(e.name+'_range')
    target_targets = document.getElementById(e.name+'_targets')
    target_cd = document.getElementById(e.name+'_cd')

    skill_fields = skills.filter(skill => skill.pk.toString() === e.value)[0].fields

    if (skill_fields) {
        console.log(skill_fields, e.name)
           target_img.style.backgroundImage = "url(/media/"+skill_fields.img+")";
    target_name.innerHTML = skill_fields.name
    target_desc.innerHTML = skill_fields.desc
    target_range.innerHTML = skill_fields.range
    target_targets.innerHTML = skill_fields.targets
    target_cd.innerHTML = skill_fields.cd

        target_div.classList.remove('hidden');

        // target_div.innerHTML = skill.fields.desc;
    } else {
        target_div.classList.add('hidden');
    }
}