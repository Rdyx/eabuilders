document.addEventListener(
	'DOMContentLoaded',
	function () {
		document
			.querySelectorAll('select[name^="skill_"]')
			.forEach((element) => updateSkillDiv(element));
		document
			.querySelectorAll('select[name^="item_"]')
			.forEach((element) => updateItemDiv(element));
	},
	false
);

function updateSkillDiv(e) {
	const target_div = document.getElementById(e.name);
	const target_content = document.getElementById(e.name + '_content');

	const target_img = document.getElementById(e.name + '_img');
	const target_img_type = document.getElementById(e.name + '_img_type');

	const target_name = document.getElementById(e.name + '_name');
	const target_desc = document.getElementById(e.name + '_desc');

	const target_range = document.getElementById(e.name + '_range');
	const target_targets = document.getElementById(e.name + '_targets');
	const target_cd = document.getElementById(e.name + '_cd');

	const skill = skills.filter((skill) => skill.pk.toString() === e.value)[0];
	if (skill) {
		const skill_fields = skill.fields;

		if (skill_fields) {
			const skill_color = skill_fields.deprecated
				? 'black'
				: skill_fields.stype[1];

			target_img.style.backgroundImage =
				'url(' +
				media_url +
				skill_fields.img +
				'), radial-gradient(' +
				skill_color +
				',' +
				skill_color +
				',black)';
			target_img_type.innerHTML = skill_fields.stype[0];

			target_name.innerHTML = skill_fields.name;
			target_name.style.color = skill_color;

			target_desc.innerHTML = skill_fields.desc;

			target_range.innerHTML = skill_fields.range;
			target_targets.innerHTML = skill_fields.targets;
			target_cd.innerHTML = skill_fields.cd;

			target_div.classList.remove('hidden');

			// Border colors
			target_div.style.borderColor = skill_color;
			target_content.style.borderColor = skill_color;
			target_name.style.borderColor = skill_color;
		} else {
			target_div.classList.add('hidden');
		}
	} else {
		target_div.classList.add('hidden');
	}
}

function updateItemDiv(e) {
	const target_div = document.getElementById(e.name);
	const target_content = document.getElementById(e.name + '_content');

	const target_img = document.querySelector('#' + e.name + '_img img');
	const race_img = document.getElementById(e.name + '_img_race');
	const material_img = document.getElementById(e.name + '_img_material');
	const target_name = document.getElementById(e.name + '_name');
	const target_desc = document.getElementById(e.name + '_desc');

	const buy = document.getElementById(e.name + '_buy');
	const sell = document.getElementById(e.name + '_sell');
	const hp = document.getElementById(e.name + '_hp');
	const phys_atk = document.getElementById(e.name + '_phys_atk');
	const mag_atk = document.getElementById(e.name + '_mag_atk');
	const phys_def = document.getElementById(e.name + '_phys_def');
	const mag_def = document.getElementById(e.name + '_mag_def');
	const acc = document.getElementById(e.name + '_acc');
	const res = document.getElementById(e.name + '_res');
	const ign_phys = document.getElementById(e.name + '_ign_phys');
	const ign_mag = document.getElementById(e.name + '_ign_mag');
	const speed = document.getElementById(e.name + '_speed');
	const crit_rate = document.getElementById(e.name + '_crit_rate');
	const crit_dmg = document.getElementById(e.name + '_crit_dmg');

	const item = items.filter((item) => item.pk.toString() === e.value)[0];
	if (item) {
		const item_fields = item.fields;

		if (item_fields) {
			const item_color = tiers_colors[item_fields.tier];

			// Remove border color from div
			tiers_colors['brown'] = 'brown-400';
			Object.values(tiers_colors).forEach((color) => {
				let border_color = 'border-' + color;
				if (target_div.classList.contains(border_color)) {
					target_name.classList.remove('text-' + color);
					target_name.classList.remove(border_color);
					target_div.classList.remove(border_color);
					target_content.classList.remove(border_color);
					target_desc.classList.remove(border_color);
				}
			});

			target_img.src = media_url + item_fields.img;
			race_img.src = media_url + item_fields.race[0];
			material_img.src = media_url + item_fields.material[0];

			target_name.innerHTML = item_fields.name;
			target_name.classList.add('text-' + item_color);

			target_desc.innerHTML = item_fields.desc;

			buy.innerHTML = item_fields.buy_cost;
			sell.innerHTML = item_fields.sell_cost;

			hp.innerHTML = item_fields.hp;
			phys_atk.innerHTML = item_fields.phys_atk;
			mag_atk.innerHTML = item_fields.mag_atk;
			phys_def.innerHTML = item_fields.phys_def;
			mag_def.innerHTML = item_fields.mag_def;
			acc.innerHTML = item_fields.acc;
			res.innerHTML = item_fields.res;
			ign_phys.innerHTML = item_fields.ign_phys;
			ign_mag.innerHTML = item_fields.ign_mag;
			speed.innerHTML = item_fields.speed;
			crit_rate.innerHTML = item_fields.crit_rate;
			crit_dmg.innerHTML = item_fields.crit_dmg;

			target_div.classList.remove('hidden');

			// Border colors
			const border_color = 'border-' + item_color;
			target_div.classList.add(border_color);
			target_content.classList.add(border_color);
			target_name.classList.add(border_color);
			target_desc.classList.add(border_color);
		} else {
			target_div.classList.add('hidden');
		}
	} else {
		target_div.classList.add('hidden');
	}
}
